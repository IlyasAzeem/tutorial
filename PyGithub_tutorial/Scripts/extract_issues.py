from github import Github, RateLimitExceededException, BadCredentialsException, BadAttributeException, \
    GithubException, UnknownObjectException, BadUserAgentException
import pandas as pd
import requests
import time
from datetime import datetime
from Scripts import config


access_token = config.ACCESS_TOKEN


def extract_project_issues(project_full_name):
    df_issues = pd.DataFrame()
    while True:
        try:
            g = Github(access_token, per_page=100, retry=20)
            repo = g.get_repo(project_full_name)
            start_time = datetime.strptime("2013-01-01 00:00:00", '%Y-%m-%d %H:%M:%S')
            end_time = datetime.strptime("2013-12-31 00:00:00", '%Y-%m-%d %H:%M:%S')
            all_issues = repo.get_issues(state='open', sort='created', direction='asc')
            counter = 0
            print(all_issues.totalCount)
            for issue in all_issues:
                while True:
                    try:
                        counter += 1
                        print(f"Loop counter {counter}")
                        print(g.rate_limiting)
                        if issue.pull_request is not None:
                            break
                        issue_comments = []
                        for comment in issue.get_comments():
                            cmt = {
                                'user': comment.user.name,
                                'user_id': comment.user.id,
                                'user_site_admin': comment.user.site_admin,
                                'body': comment.body
                            }
                            issue_comments.append(cmt)
                            print(issue.id)
                            print(issue.pull_request)

                        df_issues = df_issues.append({
                            'issue_id': issue.id,
                            'issue_number': issue.number, # issue features
                            'issue_labels': [l.name for l in issue.labels],
                            'issue_title': issue.title,
                            'issue_body': issue.body,
                            'owner': issue.user.name if issue.user is not None else '', # Issue owner features
                            'owner_username': issue.user.login if issue.user is not None else '',
                            'followers': issue.user.followers,
                            'followings': issue.user.following,
                            'contributions': issue.user.contributions,
                            'stars': issue.user.get_starred().totalCount,
                            'issue_date': issue.created_at,
                            'issue_comments': issue_comments,
                            'issueORPR': issue.pull_request
                        }, ignore_index=True)
                    except RateLimitExceededException as e:
                        print(e.status)
                        print('Rate limit exceeded')
                        time.sleep(300)
                        continue
                    except BadCredentialsException as e:
                        print(e.status)
                        print('Bad credentials exception')
                        break
                    except UnknownObjectException as e:
                        print(e.status)
                        print('Unknown object exception')
                        break
                    except GithubException as e:
                        print(e.status)
                        print('General exception')
                        break
                    except requests.exceptions.ConnectionError as e:
                        print('Retries limit exceeded')
                        print(str(e))
                        time.sleep(10)
                        continue
                    except requests.exceptions.Timeout as e:
                        print(str(e))
                        print('Time out exception')
                        time.sleep(10)
                        continue
                    break
        except RateLimitExceededException as e:
            print(e.status)
            print('Rate limit exceeded')
            time.sleep(300)
            continue
        except BadCredentialsException as e:
            print(e.status)
            print('Bad credentials exception')
            break
        except UnknownObjectException as e:
            print(e.status)
            print('Unknown object exception')
            break
        except GithubException as e:
            print(e.status)
            print('General exception')
            break
        except requests.exceptions.ConnectionError as e:
            print('Retries limit exceeded')
            print(str(e))
            time.sleep(10)
            continue
        except requests.exceptions.Timeout as e:
            print(str(e))
            print('Time out exception')
            time.sleep(10)
            continue
        break
    df_issues.to_csv('../Dataset/open_issues_1.csv', sep=',', encoding='utf-8', index=True)

extract_project_issues('PyGithub/PyGithub')