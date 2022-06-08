import QtQuick 2.7
import QtQuick.Controls 2.7

Item
{
    function updateData(data)
    {
        container.width = data.widget_width;
        container.height = data.widget_height;
        contact.width = data.icon_width;
        contact.height = data.icon_height;
        contact.text = data.contact;
    }

    id: container
    visible: true

    TextArea {
        id: contact
        visible: true
        wrapMode: TextEdit.WordWrap | TextEdit.Wrap
        anchors.fill: parent
        font.pointSize: 10
    }
}