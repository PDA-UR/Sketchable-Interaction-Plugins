import QtQuick

Item
{
    function updateData(data)
    {
        texture.width = data.icon_width;
        texture.height = data.icon_height;
        texture.source = data.img_path;
    }

    id: container
    visible: true

   Item {
       id: iconcontainer
       visible: true

       Image {
           id: texture
           anchors.left: parent.left
           anchors.top: parent.top

           visible: true
       }
    }
}