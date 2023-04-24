import QtQuick 2.7

Item {
    function updateData(data) {
        texture.width = data.img_width;
        texture.height = data.img_height;
        texture.source = data.img_path;
        texture.anchors.leftMargin = data.widget_width / 2 - texture.width / 2;
        texture.anchors.topMargin = 15;
        jingle_sequence_container.anchors.leftMargin = data.widget_width / 2 - jingle_sequence_container.width / 2;

        if (data.reset) {
            j1.color = "black";
            j2.color = "black";
            j3.color = "black";
            j4.color = "black";
            j5.color = "black";
            j6.color = "black";
            j7.color = "black";

            j1_animation.start();
            j2_animation.start();
            j3_animation.start();
            j4_animation.start();
            j5_animation.start();
            j6_animation.start();
            j7_animation.start();
        }

        if (data.hit_j1 !== undefined && data.hit_j1) {
            if(data.correct_j1) {
                j1.color = "green";
                j1_animation.start();
            } else {
                j1.color = "red";
                j1_animation.start();
            }
        }

        if (data.hit_j2 !== undefined && data.hit_j2) {
            if(data.correct_j2) {
                j2.color = "green";
                j2_animation.start();
            } else {
                j2.color = "red";
                j2_animation.start();
            }
        }

        if (data.hit_j3 !== undefined && data.hit_j3) {
            if(data.correct_j3) {
                j3.color = "green";
                j3_animation.start();
            } else {
                j3.color = "red";
                j3_animation.start();
            }
        }

        if (data.hit_j4 !== undefined && data.hit_j4) {
            if(data.correct_j4) {
                j4.color = "green";
                j4_animation.start();
            } else {
                j4.color = "red";
                j4_animation.start();
            }
        }

        if (data.hit_j5 !== undefined && data.hit_j5) {
            if(data.correct_j5) {
                j5.color = "green";
                j5_animation.start();
            } else {
                j5.color = "red";
                j5_animation.start();
            }
        }

        if (data.hit_j6 !== undefined && data.hit_j6) {
            if(data.correct_j6) {
                j6.color = "green";
                j6_animation.start();
            } else {
                j6.color = "red";
                j6_animation.start();
            }
        }

        if (data.hit_j7 !== undefined && data.hit_j7) {
            if(data.correct_j7) {
                j7.color = "green";
                j7_animation.start();
            } else {
                j7.color = "red";
                j7_animation.start();
            }
        }
    }

    id: container
    visible: true
    Image {
        id: texture
        anchors.left: parent.left
        anchors.top: parent.top
        asynchronous: true

        visible: true
    }

    Item {
        id: jingle_sequence_container
        anchors.left: parent.left
        anchors.top: texture.bottom
        width: j1.width + j2.width + j3.width + j4.width + j5.width + j6.width + j7.width

        Text {
            NumberAnimation on opacity {
                id: j1_animation
                from: 0
                to: 1
                duration: 350
            }

            id: j1
            anchors.left: jingle_sequence_container.left
            wrapMode: TextEdit.Wrap
            font.pixelSize: 64
            color: "black"

            text: "A"
            visible: true
        }

        Text {
            NumberAnimation on opacity {
                id: j2_animation
                from: 0
                to: 1
                duration: 350
            }
            id: j2
            anchors.left: j1.right
            wrapMode: TextEdit.Wrap
            font.pixelSize: 64
            color: "black"

            text: "B"
            visible: true
        }

        Text {
            NumberAnimation on opacity {
                id: j3_animation
                from: 0
                to: 1
                duration: 350
            }
            id: j3
            anchors.left: j2.right
            wrapMode: TextEdit.Wrap
            font.pixelSize: 64
            color: "black"

            text: "C"
            visible: true
        }

        Text {
            NumberAnimation on opacity {
                id: j4_animation
                from: 0
                to: 1
                duration: 350
            }
            id: j4
            anchors.left: j3.right
            wrapMode: TextEdit.Wrap
            font.pixelSize: 64
            color: "black"

            text: "D"
            visible: true
        }

        Text {
            NumberAnimation on opacity {
                id: j5_animation
                from: 0
                to: 1
                duration: 350
            }
            id: j5
            anchors.left: j4.right
            wrapMode: TextEdit.Wrap
            font.pixelSize: 64
            color: "black"

            text: "E"
            visible: true
        }

        Text {
            NumberAnimation on opacity {
                id: j6_animation
                from: 0
                to: 1
                duration: 350
            }
            id: j6
            anchors.left: j5.right
            wrapMode: TextEdit.Wrap
            font.pixelSize: 64
            color: "black"

            text: "F"
            visible: true
        }

        Text {
            NumberAnimation on opacity {
                id: j7_animation
                from: 0
                to: 1
                duration: 350
            }
            id: j7
            anchors.left: j6.right
            wrapMode: TextEdit.Wrap
            font.pixelSize: 64
            color: "black"

            text: "G"
            visible: true
        }
    }
}






