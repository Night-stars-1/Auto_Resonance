/*
* Author: Night-stars-1 nujj1042633805@gmail.com
* Date: 2024-04-21 15:11:24
* LastEditTime: 2024-04-21 15:44:58
* LastEditors: Night-stars-1 nujj1042633805@gmail.com
 */
//const core = require('@actions/core');
const { execSync } = require('child_process');

function shell(command, sep = '\n') {
    try {
        const output = execSync(command).toString();
        return output.split(sep);
    } catch (error) {
        console.error('Shell command failed:', error);
        return [];
    }
}

function getSectionTag() {
    const tags = shell("git tag --sort=-creatordate");
    return { previousTag: tags[1], currentTag: tags[0] };
}

function getCommitLog(previousTag, currentTag) {
    const output = shell(`git log ${previousTag}..${currentTag} --pretty=format:"|/|%an|-|%B|-|%h"`, '|/|');
    const message = [];
    output.forEach(line => {
        if (line) {
            const parts = line.split('|-|');
            const commitAuthor = parts[0];
            const commitMessage = parts[1];
            const commitHash = parts[2].replace(/\n/g, '');
            if (commitMessage.startsWith("Merge pull request")) return
            commitMessage.split('\n').forEach(line2 => {
                if (line2) {
                    message.push({
                        author: commitAuthor,
                        message: line2,
                        hash: commitHash
                    });
                }
            });
        }
    });
    return message;
}

function stripCommits(commits) {
    return commits.filter(commit => /^(feat|fix|refactor|test|ci|chore)/.test(commit.message));
}

function overwriteChangelog(commits) {
    const featMessage = [];
    const fixMessage = [];
    const otherMessage = [];

    commits.forEach(commit => {
        if (/^feat/.test(commit.message)) {
            featMessage.push(`* ${commit.message} by @${commit.author} in ${commit.hash}`);
        } else if (/^fix/.test(commit.message)) {
            fixMessage.push(`* ${commit.message} by @${commit.author} in ${commit.hash}`);
        } else if (/^(refactor|test|ci|chore)/.test(commit.message)) {
            otherMessage.push(`* ${commit.message} by @${commit.author} in ${commit.hash}`);
        }
    });

    let changelog = "# Changelog\n\n";
    if (featMessage.length > 0) {
        changelog += "## Features\n\n" + featMessage.join('\n') + "\n\n";
    }
    if (fixMessage.length > 0) {
        changelog += "## Fixes\n\n" + fixMessage.join('\n') + "\n\n";
    }
    if (otherMessage.length > 0) {
        changelog += "## Other\n\n" + otherMessage.join('\n') + "\n\n";
    }
    changelog += "\n> Changelog generated through the projects' GitHub Actions.";
    console.log(changelog)
    return changelog;
}

function main() {
    const { previousTag, currentTag } = getSectionTag();
    let commits = getCommitLog(previousTag, currentTag);
    commits = stripCommits(commits);
    const changelog = overwriteChangelog(commits);
    //core.setOutput('changelog', changelog)
}

main();
