import QtQuick 2.7

Item
{
    function updateData(data)
    {
        texture.width = data.width;
        texture.height = data.height;
    }

    id: container

    width:100
    height:100

    Image {
        id: texture
        anchors.left: parent.left
        anchors.top: parent.top
    }
}