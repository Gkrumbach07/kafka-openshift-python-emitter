import argparse
import logging
import os
import time
import urllib.request as urllib

from kafka import KafkaProducer


def external_file_generator(args):
    logging.info('downloading source')
    dl = urllib.urlretrieve(args.source)
    sourcefile = open(dl[0])
    logging.info('sending lines')
    for line in sourcefile.readlines():
        yield line
    logging.info('finished sending source')


def main(args):
    logging.info('brokers={}'.format(args.brokers))
    logging.info('topic={}'.format(args.topic))
    logging.info('rate={}'.format(args.rate))
    logging.info('source={}'.format(args.source))

    logging.info('creating kafka producer')
    producer = KafkaProducer(bootstrap_servers=args.brokers)

    logging.info('beginning producer loop')
    for i in external_file_generator(args):
        producer.send(args.topic, i.encode())
        time.sleep(1.0 / args.rate)


def get_arg(env, default):
    return os.getenv(env) if os.getenv(env, '') is not '' else default


def parse_args(parser):
    args = parser.parse_args()
    args.brokers = get_arg('KAFKA_BROKERS', args.brokers)
    args.topic = get_arg('KAFKA_TOPIC', args.topic)
    args.rate = get_arg('RATE', args.rate)
    args.source = get_arg('SOURCE_URI', args.source)
    return args


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    logging.info('starting kafka-python emitter')
    parser = argparse.ArgumentParser(description='emit some stuff on kafka')
    parser.add_argument(
            '--brokers',
            help='The bootstrap servers, env variable KAFKA_BROKERS',
            default='localhost:9092')
    parser.add_argument(
            '--topic',
            help='Topic to publish to, env variable KAFKA_TOPIC',
            default='bones-brigade')
    parser.add_argument(
            '--rate',
            type=int,
            help='Lines per second, env variable RATE',
            default=3)
    parser.add_argument(
            '--source',
            help='The source URI for data to emit, env variable SOURCE_URI')
    args = parse_args(parser)
    main(args)
    logging.info('exiting')
