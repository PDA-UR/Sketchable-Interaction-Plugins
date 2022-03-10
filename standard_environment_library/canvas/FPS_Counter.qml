import QtQuick 2.7

Item
{
    function updateData(data)
    {
        te.text = data["text"];
    }

    id: container
    visible: true

   Item {
       id: iconcontainer
       visible: true

       Text {
           id: te
           width: 100
           horizontalAlignment: TextEdit.AlignHCenter
           verticalAlignment: TextEdit.AlignVCenter
           text: "Hello World"
           font.family: "Helvetica"
           font.pointSize: 12
           color: "black"
           onTextChanged: REGION.set_data({text: te.text});
       }
    }
}