import QtQuick
import QtQuick.Controls


Item {
    id: container

    function updateData(data) {
        container.width = data.width - 50;
        container.height = data.height - 50;
    }

    x: 25
    y: 25

    Control {
        id: control

        readonly property color color: Qt.hsva(mousearea.angle, 1.0, 1.0, 1.0)
        property real hsvSaturation: 1.0
        property real hsvValue: 1.0
        property real ringWidth: (container.width) / 7

        anchors.centerIn: parent

        contentItem: Item {
            anchors.centerIn: parent
            implicitHeight: container.height - 50
            implicitWidth: container.width - 50

            ShaderEffect {
                id: shadereffect

                readonly property real ringWidth: control.ringWidth / width / 2
                readonly property real s: control.hsvSaturation
                readonly property real v: control.hsvValue

                fragmentShader: "res/color_picker.frag.qsb"
                height: parent.height
                width: parent.width
            }
            Rectangle {
                id: indicator

                color: 'white'
                height: width
                radius: width / 2
                width: control.ringWidth * 0.8
                x: (parent.width - width) / 2
                y: control.ringWidth * 0.1

                transform: Rotation {
                    angle: mousearea.angle * 360
                    origin.x: indicator.width / 2
                    origin.y: control.availableHeight / 2 - indicator.y
                }

                border {
                    color: Qt.lighter(control.color)
                    width: mousearea.containsPress ? 3 : 1

                    Behavior on width  {
                        NumberAnimation {
                            duration: 50
                        }
                    }
                }
            }
            Rectangle {
                anchors.centerIn: parent
                color: control.color
                height: width
                radius: width
                width: control.availableWidth * 0.3

                border {
                    color: Qt.lighter(control.color, 1.8)
                    width: 5
                }
            }
            MouseArea {
                id: mousearea

                property real angle: Math.atan2(width / 2 - mouseX, mouseY - height / 2) / 6.2831 + 0.5

                anchors.fill: parent

                onClicked: {
                    REGION.set_data({
                            "color": control.color.toString()
                        });
                }
            }
        }
    }
}