import QtQuick
import QtQuick.Controls

Item
{
    function updateData(data)
    {
        texture.width = data.widget_height;
        texture.height = data.widget_height;
        texture.source = data.img_path;
        container.width = data.widget_width;
        container.height = data.widget_height;
    }

    id: container
    visible: true

    Image {
        id: texture
        anchors.left: parent.left
        anchors.top: parent.top
        visible: true
    }

    ComboBox {
        id: cbox

        property var toggle: false

        width: 200
        anchors.top: parent.top
        anchors.right: parent.right
        anchors.bottom: parent.bottom
        anchors.left: texture.right
        anchors.topMargin: 5
        anchors.bottomMargin: 5
        anchors.leftMargin: 5
        anchors.rightMargin: 5
        focus: true

        model: ListModel {
            id: model
            ListElement { text: "Name ↑"}
            ListElement { text: "Name ↓"}
            ListElement { text: "Date ↑"}
            ListElement { text: "Date ↓"}
            ListElement { text: "File Type"}
            ListElement { text: "Addition Time ↑"}
            ListElement { text: "Addition Time ↓"}
        }

        onPressedChanged: {
            cbox.toggle = !cbox.toggle;
            REGION.set_data({down: cbox.toggle});
        }

        onCurrentIndexChanged: {
            REGION.set_data({text: cbox.model.get(currentIndex).text});
        }
    }
}