import sqlite3
import os
from datetime import datetime, timedelta
import yaml

class DepartmentAnalytics:
    def __init__(self, database_path='civic_issues.db', groq_api_key=None, config_path="config.yaml"):
        self.database_path = database_path
        self.groq_api_key = groq_api_key
        if os.path.exists(config_path):
            try:
                with open(config_path, 'r') as f:
                    config = yaml.safe_load(f)
                if config and 'groq' in config:
                    self.groq_api_key = self.groq_api_key or config['groq'].get('api_key')
            except Exception as e:
                print(f"Config loading error: {e}")
        if not self.groq_api_key:
            self.groq_api_key = "saksham"
        self.groq_client = None
        if self.groq_api_key:
            try:
                from groq import Groq
                self.groq_client = Groq(api_key=self.groq_api_key)
            except Exception as e:
                print(f"Groq initialization failed: {e}")

    def get_db_connection(self):
        conn = sqlite3.connect(self.database_path)
        conn.row_factory = sqlite3.Row
        return conn

    def get_department_overview(self):
        try:
            conn = self.get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) AS total_issues FROM issues")
            total_issues = cursor.fetchone()['total_issues']
            cursor.execute("SELECT COUNT(*) AS acknowledged FROM issues WHERE acknowledged = 1")
            acknowledged_issues = cursor.fetchone()['acknowledged']
            cursor.execute("SELECT COUNT(*) AS completed FROM issues WHERE proof_photo_url IS NOT NULL AND proof_photo_url != 'To be done'")
            completed_issues = cursor.fetchone()['completed']
            cursor.execute("SELECT COUNT(*) AS pending FROM issues WHERE acknowledged = 0")
            pending_issues = cursor.fetchone()['pending']
            cursor.execute("SELECT AVG(upvotes) AS avg_upvotes FROM issues")
            avg_upvotes = cursor.fetchone()['avg_upvotes'] or 0
            completion_rate = (completed_issues / acknowledged_issues * 100) if acknowledged_issues > 0 else 0
            acknowledgment_rate = (acknowledged_issues / total_issues * 100) if total_issues > 0 else 0
            conn.close()
            return {
                'total_issues': total_issues,
                'acknowledged_issues': acknowledged_issues,
                'completed_issues': completed_issues,
                'pending_issues': pending_issues,
                'completion_rate': round(completion_rate, 2),
                'acknowledgment_rate': round(acknowledgment_rate, 2),
                'avg_upvotes': round(avg_upvotes, 2)
            }
        except Exception as e:
            print(f"Department overview error: {e}")
            return {}

    def get_category_performance(self):
        try:
            conn = self.get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT category,
                       COUNT(*) AS total_issues,
                       SUM(CASE WHEN acknowledged = 1 THEN 1 ELSE 0 END) AS acknowledged,
                       SUM(CASE WHEN proof_photo_url IS NOT NULL AND proof_photo_url != 'To be done' THEN 1 ELSE 0 END) AS completed,
                       SUM(upvotes) AS total_upvotes,
                       AVG(upvotes) AS avg_upvotes
                FROM issues
                GROUP BY category
                ORDER BY total_issues DESC
            """)
            results = cursor.fetchall()
            conn.close()
            category_data = []
            for row in results:
                completion_rate = (row['completed'] / row['acknowledged'] * 100) if row['acknowledged'] > 0 else 0
                acknowledgment_rate = (row['acknowledged'] / row['total_issues'] * 100) if row['total_issues'] > 0 else 0
                category_data.append({
                    'category': row['category'],
                    'total_issues': row['total_issues'],
                    'acknowledged': row['acknowledged'],
                    'completed': row['completed'],
                    'completion_rate': round(completion_rate, 2),
                    'acknowledgment_rate': round(acknowledgment_rate, 2),
                    'total_upvotes': row['total_upvotes'] or 0,
                    'avg_upvotes': round(row['avg_upvotes'] or 0, 2)
                })
            return category_data
        except Exception as e:
            print(f"Category performance error: {e}")
            return []

    def get_constituency_performance(self):
        try:
            conn = self.get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT constituency,
                       COUNT(*) AS total_issues,
                       SUM(CASE WHEN acknowledged = 1 THEN 1 ELSE 0 END) AS acknowledged,
                       SUM(CASE WHEN proof_photo_url IS NOT NULL AND proof_photo_url != 'To be done' THEN 1 ELSE 0 END) AS completed,
                       SUM(upvotes) AS total_upvotes,
                       AVG(upvotes) AS avg_upvotes
                FROM issues
                GROUP BY constituency
                ORDER BY total_issues DESC
            """)
            results = cursor.fetchall()
            conn.close()
            constituency_data = []
            for row in results:
                completion_rate = (row['completed'] / row['acknowledged'] * 100) if row['acknowledged'] > 0 else 0
                acknowledgment_rate = (row['acknowledged'] / row['total_issues'] * 100) if row['total_issues'] > 0 else 0
                constituency_data.append({
                    'constituency': row['constituency'],
                    'total_issues': row['total_issues'],
                    'acknowledged': row['acknowledged'],
                    'completed': row['completed'],
                    'completion_rate': round(completion_rate, 2),
                    'acknowledgment_rate': round(acknowledgment_rate, 2),
                    'total_upvotes': row['total_upvotes'] or 0,
                    'avg_upvotes': round(row['avg_upvotes'] or 0, 2)
                })
            return constituency_data
        except Exception as e:
            print(f"Constituency performance error: {e}")
            return []

    def get_time_series_data(self, days=30):
        try:
            conn = self.get_db_connection()
            cursor = conn.cursor()
            start_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
            cursor.execute("""
                SELECT DATE(created_at) AS date,
                       COUNT(*) AS issues_reported,
                       SUM(CASE WHEN acknowledged = 1 THEN 1 ELSE 0 END) AS issues_acknowledged,
                       SUM(CASE WHEN proof_photo_url IS NOT NULL AND proof_photo_url != 'To be done' THEN 1 ELSE 0 END) AS issues_completed
                FROM issues
                WHERE DATE(created_at) >= ?
                GROUP BY DATE(created_at)
                ORDER BY DATE(created_at)
            """, (start_date,))
            results = cursor.fetchall()
            conn.close()
            time_series = []
            for row in results:
                time_series.append({
                    'date': row['date'],
                    'issues_reported': row['issues_reported'],
                    'issues_acknowledged': row['issues_acknowledged'],
                    'issues_completed': row['issues_completed']
                })
            return time_series
        except Exception as e:
            print(f"Time series error: {e}")
            return []

    def get_urgent_issues(self, limit=10):
        try:
            conn = self.get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT *,
                       julianday('now') - julianday(created_at) AS days_pending
                FROM issues
                WHERE acknowledged = 0 OR (acknowledged = 1 AND (proof_photo_url IS NULL OR proof_photo_url = 'To be done'))
                ORDER BY upvotes DESC, days_pending DESC
                LIMIT ?
            """, (limit,))
            results = cursor.fetchall()
            conn.close()
            urgent_issues = []
            for row in results:
                urgent_issues.append({
                    'id': row['id'],
                    'title': row['title'],
                    'category': row['category'],
                    'constituency': row['constituency'],
                    'upvotes': row['upvotes'],
                    'days_pending': round(row['days_pending'], 1),
                    'status': 'Acknowledged' if row['acknowledged'] else 'Pending',
                    'assigned_to': row['assigned_to'] or 'Unassigned'
                })
            return urgent_issues
        except Exception as e:
            print(f"Urgent issues error: {e}")
            return []

    def generate_ai_insight(self):
        """Return a single AI-generated insight string using Groq."""
        if not self.groq_client:
            return 'AI insights unavailable - Groq API not configured.'
        try:
            overview = self.get_department_overview()
            categories = self.get_category_performance()
            constituencies = self.get_constituency_performance()
            time_series = self.get_time_series_data()
            urgent_issues = self.get_urgent_issues(5)
            # Prepare one simple prompt
            data_summary = f"""
DEPARTMENT SUMMARY:
- Total Issues: {overview.get('total_issues', 0)}
- Completion Rate: {overview.get('completion_rate', 0)}%
- Ack Rate: {overview.get('acknowledgment_rate', 0)}%
TOP CATEGORIES: {', '.join([f"{cat['category']}: {cat['total_issues']}" for cat in categories[:3]])}
TOP CONSTITUENCIES: {', '.join([f"{const['constituency']}: {const['total_issues']}" for const in constituencies[:3]])}
RECENT (7 days): {', '.join([f"{day['date']}: {day['issues_reported']}" for day in time_series[-7:]])}
URGENT: {', '.join([f"{issue['title']} ({issue['upvotes']} upvotes, {issue['days_pending']} days)" for issue in urgent_issues[:3]])}
"""
            prompt = f"""
Based on this data:
{data_summary}
Give a single insight about departmental performance, upcoming issues, or improvement. Keep it clear and under 100 words.
"""
            insight_response = self.groq_client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="openai/gpt-oss-20b",
                max_tokens=150,
                temperature=0.7
            )
            return insight_response.choices[0].message.content.strip()
        except Exception as e:
            print(f"AI insights error: {e}")
            return f'AI insight generation failed: {str(e)}'

    def get_comprehensive_dashboard_data(self):
        """Get all dashboard data including direct AI insight."""
        return {
            'overview': self.get_department_overview(),
            'category_performance': self.get_category_performance(),
            'constituency_performance': self.get_constituency_performance(),
            'time_series': self.get_time_series_data(),
            'urgent_issues': self.get_urgent_issues(),
            'ai_insight': self.generate_ai_insight(),
            'generated_at': datetime.now().isoformat()
        }
