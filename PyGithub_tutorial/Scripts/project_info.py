from github import Github, RateLimitExceededException, BadCredentialsException, BadAttributeException, \
    GithubException, UnknownObjectException, BadUserAgentException
import pandas as pd
import requests
import time

project_list = ['apache/any23', 'apache/dubbo', 'apache/calcite', 'apache/cassandra', 'apache/cxf',
                'apache/flume', 'apache/groovy']

access_token = "paste your personal access token here"

def extract_project_info():
    df_project = pd.DataFrame()

    for project in project_list:
        g = Github(access_token)
        repo = g.get_repo(project)
        PRs = repo.get_pulls(state='all')
        df_project = df_project.append({
            'Project_ID': repo.id,
            'Name': repo.name,
            'Full_name': repo.full_name,
            'Language': repo.language,
            'Forks': repo.forks_count,
            'Stars': repo.stargazers_count,
            'Watchers': repo.subscribers_count,
            'PRs_count': PRs.totalCount
        }, ignore_index=True)
    df_project.to_csv('../Dataset/project_dataset.csv', sep=',', encoding='utf-8', index=True)

# extract_project_info()


def extract_project_info_try_except_2():
    df_project = pd.DataFrame()
    for project in project_list:
        while True:
            try:
                g = Github(access_token, retry=2, timeout=5)
                print(f'Extracting data from {project} repo')
                repo = g.get_repo(project)
                PRs = repo.get_pulls(state='all')
                df_project = df_project.append({
                    'Project_ID': repo.id,
                    'Name': repo.name,
                    'Full_name': repo.full_name,
                    'Language': repo.language,
                    'Forks': repo.forks_count,
                    'Stars': repo.stargazers_count,
                    'Watchers': repo.subscribers_count,
                    'PRs_count': PRs.totalCount
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
    df_project.to_csv('../Dataset/project_dataset_2.csv', sep=',', encoding='utf-8', index=True)


extract_project_info_try_except_2()
