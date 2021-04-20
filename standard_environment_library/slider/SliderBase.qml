import QtQuick 2.15

Item
{
    function updateData(data)
    {
        if (data.color === "r")
            rect.gradient = gradient_red.createObject(rect);
        else if (data.color === "g")
            rect.gradient = gradient_green.createObject(rect);
        else if (data.color === "b")
            rect.gradient = gradient_blue.createObject(rect);
    }

    id: container
    visible: true

    Component {
        id: gradient_red
        Gradient {
            GradientStop { position: 0.0; color: "black" }
            GradientStop { position: 1.0; color: "red" }
        }
    }

    Component {
        id: gradient_green
        Gradient {
            GradientStop { position: 0.0; color: "black" }
            GradientStop { position: 1.0; color: "green" }
        }
    }

    Component {
        id: gradient_blue
        Gradient {
            GradientStop { position: 0.0; color: "black" }
            GradientStop { position: 1.0; color: "blue" }
        }
    }

    Item {
       id: iconcontainer
       visible: true

        Rectangle {
            id: rect
            anchors.centerIn: parent
            rotation: 270
            width: 10
            height: 600
       }
    }
}