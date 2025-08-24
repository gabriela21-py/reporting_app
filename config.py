PROBLEM_QUERY = """
                SELECT jira_status, COUNT(*) AS count
                FROM jira_snapshot
                WHERE issue_type = 'Problem Report'
                  AND _is_current
                GROUP BY jira_status
                ORDER BY jira_status; \
                """

PRIORITY_QUERY = """
                 SELECT COUNT(*) AS count, priority
                 FROM jira_snapshot
                 WHERE issue_type = 'Problem Report'
                   AND _is_current = true
                 GROUP BY priority; \
                 """

SEVERITY_QUERY = """
                 SELECT COUNT(*) AS count, severity
                 FROM jira_snapshot
                 WHERE issue_type = 'Problem Report'
                   AND _is_current = true
                 GROUP BY severity; \
                 """

UPDATE_DROPDOWN_QUERY = """
                        SELECT DISTINCT agile_team
                        FROM jira_snapshot
                        WHERE _is_current = true
                          AND agile_team IS NOT NULL
                        ORDER BY agile_team; \
                        """

FEATURES_QUERY = """
                 SELECT jira_status AS status,
                        COUNT(*) AS count
                 FROM jira_snapshot
                 WHERE _is_current = FALSE
                 GROUP BY jira_status
                 ORDER BY jira_status; \
                 """
