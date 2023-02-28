import QtQuick 2.7
import QtQuick.Controls 2.15

Item
{
    function updateData(data)
    {
        container.width = data.width;
        container.height = data.height;
        content.text = data.text;
    }

    id: container
    visible: true

    TextArea {
        focus: false
        width: parent.width
        height: parent.height
        horizontalAlignment: TextEdit.AlignHCenter
        verticalAlignment: TextEdit.AlignVCenter
        id: content
        font.pixelSize: Math.min(content.width, content.height) / 1.5
        text: ""
        placeholderText: "PostIt"
        font.family: "Helvetica"
        wrapMode: TextEdit.Fit | TextEdit.Wrap
        color: "black"
        background: Rectangle {
            color: "transparent"
        }

        function adjustFontSize() {
            if (content.lineCount > 1) {
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