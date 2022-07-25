---
# HAR AI FRAMEWORK
- [Deep learning networks for human activity recognition](#Deep-learning-networks-for-human-activity-recognition)
    - [Pre-process and training framework in tensorflow](#Pre-process-and-training-framework-in-tensorflow)
    - [Docker architecture](#Docker-architecture)
    - [Pre-process environment](#Pre-process-environment)
    - [Training environment](#Training-environment)
    - [Inference environment](#Inference-environment)
    - [Delivery](#Delivery)
- [What is this project all about?](#What-is-this-project-all-about?)
- [Contact](#Contact)
- [Licensing](#Licensing)
## Deep learning networks for human activity recognition

### Pre-process and training framework in tensorflow

This project provides a docker based framework which aims to expedite the resolution of the ***human activity recognition & classification*** (HAR) problem. Three separate components are provided for this purpose:

- Pre-process environment.
- Training environment.
- Inference environment.

While the ***training environment*** provides a generic utility for neural network's automatic setup, the ***pre-process environment*** has its focus on pre-processing human activity datasets (time series datatables from human body sensors).
On the other hand, the ***inference environment*** serves a rest API based on Flask which loads a trained neural network and answers for human movement classification requests. This API is also focused on the human activity classification problem, but can be easily tuned for a more generic purpose. To know more about flask you can visit the [official flask webpage](https://flask.palletsprojects.com/en/1.1.x/).

Pre-requirements:

- Docker v17
- GNU Make

The following instruction launches both environments:

```sh
# Launch the hole development environment.
make develenv-up

# Launch the hole development environment recreating images.
make develenv-up-recreate
```

You can also use one of these instructions to launch a single component:
```sh
# Launch only the preprocess environment.
make preprocess-up

# Launch train environment.
make train-up

# Launch the inference API.
make inference-up
```

Also, `make help` utility is available to the developer.

### Docker architecture

For the reference there is a generic view of the architecture:

![Usage_schema](doc/images/docker-architecture.png)

As you'd have noticed, the ***inference environment*** has little to do with the rest of the architecture and can be treated as an individual component. Ideally, this component will be the only one deployed in a production environment.

More information can be found here: [data structure documentation](framework)

### Pre-process environment

```sh
# Enter the pre-process environment
make preprocess-sh
```

The guide for this environment can be found here: [pre-process environment documentation](framework/pre-process)

### Training environment

```sh
# Enter the training environment
make train-sh
```

The guide for this environment can be found here: [training environment documentation](framework/train)

### Inference environment

```sh
# Enter the pre-process environment
make inference-sh
```

Although, the most useful command in this environment may be:

```sh
# Display container logs
docker logs -f inference
```

The guide for this environment can be found here: [inference environment documentation](framework/inference)

### Delivery
This framework also provides [Jenkins](https://www.jenkins.io/) pipelines to smoothly run pre-process and training phases: [more info](delivery/jenkins).

## What is this project all about?

This project is the final assignment for Gonzalo Pardo Villalibre. The aim will be to detect which activity is a certain subject performing, minimizing the number of sensors needed. Therefore the student will take advantage of the use of NN (neural networks) from different types such as CNN (convolutional networks) or RNN (recurrent networks) such LSTM.

On this journey the developer decided to not only solve the concrete problem, but also to create a reusable framework making the process easier for future investigators.

More info about specific problem can be found here: [more info](doc/documents/this-problem.md)

## Contact

You can contact the creator via e-mail at: `gonzalopmb@gmail.com`

## Licensing

MIT License

Copyright (c) 2021 Gonzalo Pardo Villalibre

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

