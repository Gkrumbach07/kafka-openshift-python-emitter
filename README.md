# kafka-python-emitter
A Python application skeleton for emitting to an Apache Kafka topic using a cron job

This application will simply take a source URI for a file and then send the
lines from that file to the topic and brokers specified through the environment
variables.

## Deploying on OpenShift

These instructions show how to deploy the emitter on [OpenShift](https://okd.io)
using the [command line client tool](https://docs.okd.io/latest/cli_reference/get_started_cli.html).

### Prerequisites

* A terminal shell with the OpenShift client tool (`oc`) available.

* An active login to an OpenShift project

### Procedure

* Launch the emitter using the following commands
 ### Kafka Producer
Next we create the Kafka producer. We will use a cron-job to accomplish this. We will run through a series of commands to create the build config and cron config files. First we need to create a service account that will run the cron job. The full in depth process can be found [here](https://github.com/clcollins/openshift-cronjob-example), but the following commands are all that is needed to deploy.
```
oc create serviceaccount py-cron

oc create role pod-lister --verb=list --resource=pods,namespaces
oc policy add-role-to-user pod-lister --role-namespace=py-cron system:serviceaccounts:py-cron:py-cron

oc create imagestream py-cron

oc create -f https://raw.githubusercontent.com/Gkrumbach07/kafka-openshift-python-emitter/master/buildConfig.yml

oc set env BuildConfig/py-cron KAFKA_BROKERS=my-cluster-kafka-brokers:9092
oc set env BuildConfig/py-cron KAFKA_TOPIC=forecast
oc set env BuildConfig/py-cron USER_FUNCTION_URI=https://github.com/Gkrumbach07/kafka-openshift-python-emitter/blob/master/examples/emitter.py

oc start-build BuildConfig/py-cron

oc create -f https://raw.githubusercontent.com/Gkrumbach07/kafka-openshift-python-emitter/master/cronJob.yml
```
You will need to adjust the `KAFKA_BROKERS` and `KAFKA_TOPICS` variables to
match your configured Kafka deployment and desired topic. The `SOURCE_URI`
environment variable allows you to specify the source file to emit from.

## Customizing the emitter function

You can change the behavior of the emitter by supplying a generator function
that will get polled at the rate specified. The user defined function that you
supply must be a generator that accepts a single argument and returns a string.
The arguments provided will be a wrapper to the application configuration. For
an example see the [emitter.py](examples/emitter.py) file.

### User defined function API

The API for creating a user defined function is fairly simple, there are three
rules to crafting a function:

1. There must be a top-level function named `user_defined_function`. This
   is the main entry point into your feature, the main application will look
   for this function.
1. Your function must accept a single argument. The function will be passed
   a namespace object containing the application configuration options.
1. Your function must return either a string. That string will get emitted
   onto the kafka topic for the application.
