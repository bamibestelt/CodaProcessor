import argparse

from http_task import fetch_coda_links
from rabbit import start_listen_request_queue

test_rss = "https://deviesdevelopment.github.io/blog/posts/index.xml"


def main():
    print("Coda decoder starting...")
    args = parse_arguments()
    if args.t:
        links = fetch_coda_links()
        print(f"links size: {len(links)}")
        print(f"obtained links: {links}")
        return
    start_listen_request_queue()


def parse_arguments():
    parser = argparse.ArgumentParser(description='Run Coda links decoder.')
    parser.add_argument("-t",
                        action='store_true',
                        help='Use this flag to use test links defined in the code.')

    parser.add_argument("-r",
                        action='store_true',
                        help='Use this flag to receive links from RabbitMQ message.')

    return parser.parse_args()


if __name__ == '__main__':
    main()
