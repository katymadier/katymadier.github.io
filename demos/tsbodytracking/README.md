# Tensorflow PoseNet body tracking for virtual reality

<img src="tsbodytracking.gif" alt="VRDemo" style="width: 600px;"/>

## The Project [Work-in-Progress]

This is a demo created for use in my Master's Thesis. The thesis focuses on analyzing the social VR landscape to better understand how to make co-located VR experiences more collaborative and social.

### Demo Goals

This purpose of this demo is to provide a way for mobile VR users to engage in VR experiences together simply by placing their phones in a low-cost VR device like Google cardboard. By using phone camera-based body tracking, VR users do not have to instrument an environment to get realistic body representation in the virtual environment.

We will use this demo as a part of a user study to discover if body representation in co-located social VR experiences encourages collaboration and increases feelings of togetherness. Scenarios will be developed to study multiple co-located VR participants and co-located VR + non-VR participants. 

### Additional work to be done

* Use additional sensor or marker to identify z coordinate.
* Animate a 3D model with poses.
* Add facial expression tracking of both VR and non-VR participants.
* Provide multi-user support.
* Prototype will be configurable to support multiple study activities. 


### Demo

* [live Demo](https://katymadier.github.io/demos/tsbodytracking/)<br>
* [Video](https://www.useloom.com/share/eed34684bea44e429b0f9992f2712f6f)<br>


## Built With

* [Tensorflow.js](https://js.tensorflow.org/) - Javascript library for training & deploying ML models in the browser and on Node.js.
* [Tensorflow.js PoseNet](https://github.com/tensorflow/tfjs-models/tree/master/posenet) - In browser human body pose estimation model.
* [A-Frame](https://aframe.io/) - The web framework used web-based VR prototypes.


## Authors

* **Katy Madier** - [katymadier.com](https://katymadier.com)


## Acknowledgments

Thanks to my advisor, Professor Michael Nebeling, and the University of Michigan Information Interaction Lab for supporting the work in my master's thesis.
