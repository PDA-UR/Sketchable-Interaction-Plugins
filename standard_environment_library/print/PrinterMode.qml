import QtQuick

Item
{
    function updateData(data)
    {
        printername.width = data.icon_width;
        printername.height = data.icon_height;
        printername.text = data.text;
    }

    id: container
    visible: true

    Text {
        id: printername
        visible: true

        fontSizeMode: Text.Fit
        minimumPixelSize: 16
        color: "black"
        horizontalAlignment: Text.AlignHCenter
        verticalAlignment: Text.AlignVCenter

        wrapMode: TextEdit.Wrap
    }
}