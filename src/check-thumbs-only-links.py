#!/usr/bin/python3

from slackviewerfiles.utils.slack_utils import slack_get_priv_path


def load_all_links(link_file):
    with open(link_file) as f:
        return f.readlines()


def get_all_thumbs(lines, to_file):
    all_lines = '\n'.join(lines)
    missing_priv_thims = []
    for line in lines:
        priv_path, thumb_found = slack_get_priv_path(line)
        if priv_path is not None and all_lines.find(priv_path) == -1:
            missing_priv_thims.append(line)

    with open(to_file, 'w') as f:
        f.writelines(missing_priv_thims)


if __name__ == '__main__':
    lines = load_all_links('../links/slack-links.txt')
    get_all_thumbs(lines, '../links/slack-links-thumbs-only.txt')
