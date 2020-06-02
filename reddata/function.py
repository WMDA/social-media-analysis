import yaml
import argparse


def load_config(config_file = "config.yaml"):
    config_yml = open(config_file)
    config = yaml.load(config_yml, yaml.SafeLoader)
    return config

def get_arguments():
    parse = argparse.ArgumentParser()
    parse.add_argument("-t", "--topics", dest='topics', nargs='*', help='Topics in for praw to search reddit')
    parse.add_argument("-c","--comments", dest='comments', help='Selects number of comments for praw to limit to.')
    parse.add_argument("-config",help="Uses config.yaml file instead of providing options, doesn't take any arguments but needs config.yaml file (provided with package)",action="store_true")
    parse.add_argument("-csv", help="Saves output to CSV, needs a directory to save csv to")
    parse.add_argument("-n","--name", dest='name', help="Gives the file a name, if this option is not used in conjunction with -csv then file will be called reddit_database")
    options= parse.parse_args()
    if options.config:
        config = load_config()
        options.topics=config["topics"]
        options.comments= config["comments"]
        return options
    elif not options.topics or not options.comments:
        parse.error(">> Needs topic and number of comment. Use -t and put topics and -c to put number of comments or use -config. Use -h for more information.")
    else:
        return options


def print_output(topic,comments,*args):
    print('\n','Searching reddit for','\n',topic)
    print('\n','Limiting comments to','\n', comments)
