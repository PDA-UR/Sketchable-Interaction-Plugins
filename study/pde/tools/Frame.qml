import QtQuick 2.7
import QtQuick.Controls 2.15

Item
{
    function updateData(data) {
        container.width = data.width;
        container.height = data.height;
    }

    x: 0
    y: 0

    id: container
    visible: true

    TextArea {
        width: container.width
        height: container.height
        anchors.top: container.top
        anchors.left: container.left
        anchors.right: container.right
        id: content
        font.pixelSize: Math.min(content.width, content.height) / 2
        text: ""
        placeholderText: "Frame"
        font.family: "Helvetica"
        wrapMode: TextEdit.Fit | TextEdit.Wrap
        color: "black"
        background: Rectangle {
            color: "transparent"
        }

        function adjustFontSize() {
            if (content.lineCount > 3) {
                content.font.pixelSize =  Math.min(content.width, content.height) / 5;
                var newPixelSize = content.font.pixelSize - 1;
                while (newPixelSize > 0 && content.height < contentHeight) {
                    newPixelSize--;
                    content.font.pixelSize = newPixelSize;
                }
            }
        }

        onTextChanged: {
            adjustFontSize();
        }

        onWidthChanged: {
            adjustFontSize();
        }

        onHeightChanged: {
            adjustFontSize();
        }
    }
}