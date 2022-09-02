import QtQuick 2.7

Item {
    function updateData(data)
    {
        components.texture.width = data.img_width;
        components.texture.height = data.img_height;
        components.texture.source = data.img_path;
        components.texture.anchors.leftMargin = data.width / 2 - components.texture.width / 2;
        components.texture.anchors.topMargin = data.height / 2 - components.texture.height * 1.25;
        components.texture.x = data.x;
        components.texture.y = data.y;

        if(data.visible)
            createAnimation.start();

        components.hover_text.visible = data.visible;

        components.hover_text.text = data.text;

        container.width = data.width;
        container.height = data.height;

        components.hover_text.width = data.width;
        components.hover_text.height = data.height;
    }

    property alias components: loader.item

    id: container
    visible: true

     Loader {
        id: loader
        anchors.fill: parent
        sourceComponent: component
        asynchronous: true
      }

    Component {
        id: component

        Item {
            property alias texture: tex
            property alias hover_text: hov_text

            Text {
                NumberAnimation on opacity {
                    id: createAnimation
                    from: 0
                    to: 1
                    duration: 350
                }

                id: hov_text
                visible: false

                fontSizeMode: Text.Wrap
                font.pixelSize: 18
                color: "black"
                horizontalAlignment: Text.AlignHCenter
                anchors.top: parent.top

                anchors.topMargin: hover_text.height / 2 + hover_text.height / 12

                wrapMode: Text.Wrap
            }

            Image {
                id: tex
                asynchronous: true
                visible: true
            }
        }
    }
}