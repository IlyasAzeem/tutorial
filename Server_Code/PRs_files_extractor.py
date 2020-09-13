from github import Github, RateLimitExceededException, BadCredentialsException, BadAttributeException, \
    GithubException, UnknownObjectException, BadUserAgentException
# import pandas as pd
import requests
import time
import json
import os
from os import listdir
from os.path import join
import csv


# df = pd.read_csv("../PR_Files/java_projects_PRs_ids.csv", sep=',', encoding='utf-8')
# raw_file = "../PR_Files/java_projects_PRs_ids.csv"

access_token = "2e2cdf299bebac62f8205abde889f51d67b1990b"

parent_directory = "PR_Files/"
projects_file_path = "Projects_files_for_server/first/"

def read_single_file(file_path):
    project_file = open(file_path, "r")
    counter=1
    for line in project_file.readlines():
        load_dict = json.loads(line)
        print(counter)
        print(load_dict)
        counter+=1

# def create_projects_list():
#     print('Projects list creation in progress')
#     for file in listdir(projects_file_path):
#         print(f'Processing project {file}')
#         df_projects_PRs_ID = pd.DataFrame()
#         project_file = open(join(projects_file_path, file), "r")
#         for line in project_file.readlines():
#             load_dict = json.loads(line)
#             id = Extract_Id_From_Url(load_dict['url'])
#             project_name = load_dict['url'].split('/')[4]+'/'+load_dict['url'].split('/')[5]
#             url = load_dict['url']
#             df_projects_PRs_ID = df_projects_PRs_ID.append({
#                "PR_ID": id,
#                 'project': project_name,
#                 'url': url,
#             }, ignore_index=True)
#         print(df_projects_PRs_ID.shape)
#         df_projects_PRs_ID.to_csv('PR_Files/Projects_files_for_server/'+load_dict['url'].split('/')[5]+'.csv',
#                                   sep=',', index=False)


def Extract_Id_From_Url(url):
    id = url.split('/')[7]
    return id

def Extract_Project_Name_From_Url(url):
    project_name = url.split('/')[5]
    return project_name

def get_PR_files(project_full_name, file_path):
    project_folder_path = join(parent_directory, project_full_name.split('/')[1])
    os.mkdir(project_folder_path)
    while True:
        try:
            g = Github(access_token, per_page=100)
            repo = g.get_repo(project_full_name)
            print(f'Extracting files')
            file = open(file_path, "r")
            data = csv.reader(file)
            next(data)
            for line in data:
                try:
                    project_name = project_full_name.split('/')[1]
                    pr = repo.get_pull(int(line[0]))
                    # Extracting files of the current PRs
                    PR_folder = project_name+'-'+line[0]
                    path = os.path.join(project_folder_path, PR_folder)
                    os.mkdir(path)
                    for f in pr.get_files():
                        print("Directory {} created".format(PR_folder))
                        # os.system("wget -P "+path+"/ {0}".format(f.raw_url))
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

if __name__ == '__main__':
    print('Start extraction')
    # get_PR_files()
    # create_projects_list()

    for file in listdir(projects_file_path):
        print(f'Processing project {file}')
        project_file = open(join(projects_file_path, file), "r")
        data = csv.reader(project_file)
        next(data)
        row = next(data)
        # print(row)
        print(row[1], join(projects_file_path, file))
        get_PR_files(row[1], join(projects_file_path, file))
