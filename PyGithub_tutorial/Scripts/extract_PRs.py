from github import Github, RateLimitExceededException, BadCredentialsException, BadAttributeException, \
    GithubException, UnknownObjectException, BadUserAgentException
import pandas as pd
import requests
import time

access_token = "paste your personal access token here"

def extract_project_PRs(project_full_name):
    df_PRs = pd.DataFrame()
    while True:
        try:
            g = Github(access_token, retry=10, timeout=15, per_page=100)
            print(f'Extracting data from {project_full_name} repo')
            repo = g.get_repo(project_full_name)
            PRs_list = repo.get_pulls(state='closed', sort='created', base='master')

            for pr in PRs_list:
                try:
                    print(g.rate_limiting)
                    print(f'Extracting data from PR # {pr.number}')
                    # Review Comments on the Pull requests
                    review_comments = []
                    if pr.get_comments().totalCount>0:
                        for comment in pr.get_comments():
                            cmt = {
                                'comment_id': comment.id,
                                'comment_body': comment.body,
                                'comment_created': comment.created_at,
                                'commenter': comment.user.login,
                                'type': comment.user.type
                            }
                            review_comments.append(cmt)
                    df_PRs = df_PRs.append({
                        'pr_id': pr.id, # PRs features
                        'pr_title': pr.title,
                        'pr_body': pr.body,
                        'pr_number': pr.number,
                        'pr_url': pr.url,
                        'pr_html_url': pr.html_url,
                        'pr_state': pr.state,
                        'additions': pr.additions,
                        'deletions': pr.deletions,
                        'pr_changed_files': pr.changed_files,
                        'pr_commits_count': pr.commits,
                        'pr_comments_count': pr.comments,
                        'pr_review_comments_count': pr.review_comments,
                        'pr_labels_count': len([l.name for l in pr.labels]),
                        'pr_assignees_count': len(pr.assignees),
                        'pr_labels': [l.name for l in pr.labels],
                        'pr_created_at': pr.created_at,
                        'pr_closed_at': pr.closed_at,
                        'pr_review_comments': review_comments,
                        'contributor': pr.user.name,  # Contributor's information
                        'contributor_id': pr.user.id,
                        'contributor_email': pr.user.email,
                        'contributor_type': pr.user.type,
                        'contributor_public_repos': pr.user.public_repos,
                        'contributor_private_repos': pr.user.owned_private_repos,
                        'contributor_followings': pr.user.following,
                        'contributor_followers': pr.user.followers,
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
    df_PRs.to_csv('../Dataset/PRs_dataset_2.csv', sep=',', encoding='utf-8', index=True)

extract_project_PRs('apache/any23')