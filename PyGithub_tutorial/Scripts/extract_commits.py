from github import Github, RateLimitExceededException, BadCredentialsException, BadAttributeException, \
    GithubException, UnknownObjectException, BadUserAgentException
import pandas as pd
import requests
import time
from datetime import datetime
from Scripts import config


access_token = config.get_access_token()


def extract_project_commits(project_full_name):
    df_commits = pd.DataFrame()
    while True:
        try:
            g = Github(access_token, per_page=100, retry=20)
            repo = g.get_repo(project_full_name)
            start_time = datetime.strptime("2010-01-01 00:00:00", '%Y-%m-%d %H:%M:%S')
            end_time = datetime.strptime("2012-3-31 00:00:00", '%Y-%m-%d %H:%M:%S')
            all_commits = repo.get_commits(author='s-t-e-v-e-n-k')
            counter = 0
            print(all_commits.totalCount)
            for commit in all_commits:
                while True:
                    try:
                        counter += 1
                        print(f"Loop counter {counter}")
                        print(g.rate_limiting)
                        df_commits = df_commits.append({
                            'commit_sha': commit.sha,
                            'committer_username': commit.author.login if commit.author is not None else '',
                            'committer_name': commit.author.name if commit.author is not None else '',
                            'committer_email': commit.author.email if commit.author is not None else '',
                            'commit_date': commit.author.created_at if commit.author is not None else '',
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
    df_commits.to_csv('../Dataset/commits_author_1.csv', sep=',', encoding='utf-8', index=True)

extract_project_commits('PyGithub/PyGithub')