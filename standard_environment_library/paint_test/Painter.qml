import QtQuick 2.7

Item
{
    function updateData(data)
    {

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