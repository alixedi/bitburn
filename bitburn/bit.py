#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import requests
import pprint

def get_team_repos(team, uname, pwd):
    """Given the team name and auth credentials, returns all repositories
    for that team"""
    repos = []
    while True:
        url = 'https://bitbucket.org/api/2.0/teams/%s/repositories' % team
        r = requests.get(url, auth=(uname, pwd))
        rj = r.json()
        repos += rj['values']
        if not 'next' in rj:
            break
    return repos
                
def get_repo_issues(team, repo, uname, pwd):
    """Given the repo name and auth credentials, returns all issues
    for that repo"""
    url = 'https://bitbucket.org/api/1.0/repositories/%s/%s/issues?accountname=%s&repo_slug=%s' % (team, repo, team, repo)
    r = requests.get(url, auth=(uname, pwd))
    rj = r.json()
    return rj['issues']

def get_issue_comments(team, repo, issue, uname, pwd):
    """Given team, repo, issue and auth credentials, return all comments"""
    url = 'https://bitbucket.org/api/1.0/repositories/%s/%s/issues/%s/comments' % (team, repo, issue)
    r = requests.get(url, auth=(uname, pwd))
    rj = r.json()
    return rj

def parse_issue(issue):
    """Given an issue, return data that needs saving"""
    from pyparsing import Word, Suppress, Literal, OneOrMore, Optional, nums, printables
    sprint = (Literal('Sprint') | Literal('sprint')) + Word(nums)
    points = Suppress(Literal('(')) + Word(nums) + Suppress(Literal(')'))
    deadline = Suppress(Literal('<')) + Word(nums)
    name = OneOrMore(Word(printables))
    title = Optional(sprint).setResultsName("sprint") + \
            Optional(name).setResultsName("name") + \
            Optional(deadline).setResultsName("deadline") + \
            points.setResultsName("points")    
    try:
        _, r = title.parseString(issue['title'])
        print r
    except:
        pass



def bit(args):
    """Get scrum data for given Bitbucket team."""
    # get all repositories for the team
    repos = get_team_repos(args.team, args.uname, args.pwd)
    # get issues
    data = []
    for repo in repos:
        issues = get_repo_issues(args.team, repo['name'], args.uname, args.pwd)
        for issue in issues:
            comments = get_issue_comments(args.team, repo['name'], issue['local_id'], args.uname, args.pwd)
            data.append([repo['name'], issue, comments])
    #pprint.pprint(data)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Fetch data from Bitbucket repository.')
    parser.add_argument('team', help='Team name.')
    parser.add_argument('uname', help='Bitbucket username.')
    parser.add_argument('pwd', help='Bitbucket password.')
    args = parser.parse_args()
    bit(args)
