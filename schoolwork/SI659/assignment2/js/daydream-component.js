
// remixed from aframe listener code
// https://github.com/aframevr/aframe/blob/master/docs/introduction/interactions-and-controllers.md
AFRAME.registerComponent("daydream-listener", {
  schema: {
    action: {
      swipe: {type:'string', default: "left"},
      touch: {type:'string', default: "left"},
      buttonclick: {type:'bool', default: false},
      buttontap: {type:'bool', default:false},
      trackpadup: {type:'bool', default:false},
      trackpaddown: {type:'bool', default:false}
    }
  },
  update: function() {
    var start;
    var end;
    var action = this.data;
    var controller = this.el;
    controller.addEventListener("touchstart", (e) => {
      // console.log(e)
      //movement start
      start = e.target.components["tracked-controls"].controller.axes[0];
      if (start <.79){
        action = {touch:"left"};
        controller.emit('action', action);
      }
      if (start > -.79){
        action = {touch:"right"};
        controller.emit('action', action);
      }

      //gamepadButton
      if (e.target.components["tracked-controls"].controller.buttons[0].touched==true){
        action={buttontap:true}
      }
    });
    controller.addEventListener("touchend", (e) => {
      // console.log(e)
      end = e.target.components["tracked-controls"].controller.axes[0];

    });
    controller.addEventListener("trackpaddown", (e) => {
      action={trackpaddown:true}
      controller.emit('action', action);
    });
    controller.addEventListener("trackpadup", (e) => {
      action={trackpadup:true}
      controller.emit('action', action);
    });
  },
});

// remixed from aframe instructions
AFRAME.registerComponent('collider-check', {
  dependencies: ['raycaster'],
  schema: {
    intersection: {
      objectid: {type:'string', default:"name"},
      location: {type:'array', default: {x:0, y:0, z:0}},
    }
  },
  init: function () {
    var intersection = this.data;
    var controller = this.el;
    var location;
    var name;
    var object;
    var objectclassname;

    controller.addEventListener('raycaster-intersection', function (e) {
       for (x in e.detail.els){
         console.log("intersected #" + e.detail.els[x].id)
          object = document.querySelector("#" + e.detail.els[x].id)
          object.emit('hover')
          objectclassname = e.detail.els[x].className
       }
    });
    controller.addEventListener('trackpaddown', function(e) {
      console.log(e)
      if (e.detail.intersectedEl){
        name =e.detail.intersectedEl.id;
        location = e.detail.intersection.point;
        objectclassname =e.detail.intersectedEl.className;
        clickedobject = document.querySelector("#" + e.detail.intersectedEl.id)
        clickedobject.emit('click')
        if (e.detail.intersectedEl.className){
          objectclassname = e.detail.intersectedEl.className;
          console.log(name, location)
          if (objectclassname == "moveable"){
            intersection = {
              objectid:name,
              location:location
            }
            controller.emit('intersection', intersection);
          }
        }
      }
    })
  }
});
//
//
//
//
//
//
// // remixed from other code
// AFRAME.registerComponent("daydream-listener", {
//   schema: {
//     action: {
//       swipe: {type:'string', default: "left"},
//       touch: {type:'string', default: "left"},
//       buttonclick: {type:'bool', default: false},
//       buttontap: {type:'bool', default:false},
//       trackpadup: {type:'bool', default:false},
//       trackpaddown: {type:'bool', default:false}
//     }
//   },
//   update: function() {
//     var xAxis;
//     var yAxis;
//     var action = this.data;
//     var controller = this.el;
//     controller.addEventListener("touchstart", (e) => {
//       // AFRAME.log("touchstarted")
//       xAxis = e.target.components['tracked-controls'].controller.axes[0]
//       yAxis = e.target.components['tracked-controls'].controller.axes[1]
//       // left side
//       if (xAxis < -.7 && yAxis > -.3 && yAxis <.3){
//         // AFRAME.log("started at left")
//         // AFRAME.log(xAxis)
//         action = {touch:"left"};
//         controller.emit('action', action);
//       }
//       // right side
//       if (xAxis > .7 && yAxis > -.3 && yAxis <.3){
//         // AFRAME.log("started at right")
//         // AFRAME.log(xAxis)
//         action = {touch:"right"};
//         controller.emit('action', action);
//       }
//       // top
//       if (yAxis < -.7 && xAxis > -.3 && xAxis <.3){
//         // AFRAME.log("started at top")
//         // AFRAME.log(yAxis)
//         action = {touch:"top"};
//         controller.emit('action', action);
//       }
//       // bottom
//       if (yAxis > .7 && xAxis > -.3 && xAxis <.3){
//         // AFRAME.log("started at bottom")
//         // AFRAME.log(yAxis)
//         action = {touch:"bottom"};
//         controller.emit('action', action);
//       }
//     });
//     controller.addEventListener("touchend", (e) => {
//       // AFRAME.log("touchended")
//       xAxis = e.target.components['tracked-controls'].controller.axes[0]
//       yAxis = e.target.components['tracked-controls'].controller.axes[1]
//       // left side
//       if (xAxis < -.7 && yAxis > -.3 && yAxis <.3){
//         // AFRAME.log("ended at left")
//         // AFRAME.log(xAxis)
//         action = {touch:"left"};
//         controller.emit('action', action);
//       }
//       // right side
//       if (xAxis > .7 && yAxis > -.3 && yAxis <.3){
//         // AFRAME.log("ended at right")
//         // AFRAME.log(xAxis)
//         action = {touch:"right"};
//         controller.emit('action', action);
//       }
//       // top
//       if (yAxis < -.7 && xAxis > -.3 && xAxis <.3){
//         // AFRAME.log("ended at top")
//         // AFRAME.log(yAxis)
//         action = {touch:"top"};
//         controller.emit('action', action);
//       }
//       // bottom
//       if (yAxis > .7 && xAxis > -.3 && xAxis <.3){
//         // AFRAME.log("ended at bottom")
//         // AFRAME.log(yAxis)
//         action = {touch:"bottom"};
//         controller.emit('action', action);
//       }
//     });
//
//     controller.addEventListener("trackpadtouchstart", (e) => {
//       //movement start
//       xAxis = e.target.components['tracked-controls'].controller.axes[0]
//       yAxis = e.target.components['tracked-controls'].controller.axes[1]
//       // AFRAME.log("start" + start);
//
//       // left side
//       if (xAxis < -.7 && yAxis > -.3 && yAxis <.3){
//         // AFRAME.log("touched left")
//         // AFRAME.log(xAxis)
//         action = {touch:"left"};
//         controller.emit('action', action);
//       }
//       // right side
//       if (xAxis > .7 && yAxis > -.3 && yAxis <.3){
//         // AFRAME.log("touched right")
//         // AFRAME.log(xAxis)
//         action = {touch:"right"};
//         controller.emit('action', action);
//       }
//       // top
//       if (yAxis < -.7 && xAxis > -.3 && xAxis <.3){
//         // AFRAME.log("touched top")
//         // AFRAME.log(yAxis)
//         action = {touch:"top"};
//         controller.emit('action', action);
//       }
//       // bottom
//       if (yAxis > .7 && xAxis > -.3 && xAxis <.3){
//         // AFRAME.log("touched bottom")
//         // AFRAME.log(yAxis)
//         action = {touch:"bottom"};
//         controller.emit('action', action);
//       }
//     });
//
//     // controller.addEventListener("trackpadtouchend", (e) => {
//     //     end = e.target.components['tracked-controls'].controller.axes[0] + " " + e.target.components['tracked-controls'].controller.axes[1]
//     //     AFRAME.log("end" + end);
//     // });
//     controller.addEventListener("trackpaddown", (e) => {
//       // AFRAME.log("clicked" + e.target.components['tracked-controls'].controller.axes[0] + " " + e.target.components['tracked-controls'].controller.axes[1]);
//       // createbug("clicked", e);
//       action={trackpaddown:true}
//       controller.emit('action', action);
//     });
//     controller.addEventListener("trackpadup", (e) => {
//       // AFRAME.log("released" + e.target.components['tracked-controls'].controller.axes[0] + " " + e.target.components['tracked-controls'].controller.axes[1]);
//       // createbug("released", e);
//       action={trackpadup:true}
//       controller.emit('action', action);
//     });
//   },
// });
//
// // do some stuff with the trackpad actions
// // window.addEventListener('action', function(e){
// //     if (e.detail.touch == "left"){
// //       camera.object3D.rotation.y += Math.PI/8;
// //     }
// //     if (e.detail.touch == "right") {
// //       camera.object3D.rotation.y -= Math.PI/8;
// //     }
// //     if (e.detail.trackpaddown==true){
// //       // console.log("trackpad pressed down")
// //
// //     }
// //     if (e.detail.trackpadup==true){
// //       // console.log("trackpad released")
// //     }
// // });
