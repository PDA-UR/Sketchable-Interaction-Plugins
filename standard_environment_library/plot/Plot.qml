import QtQuick 2.7
import siqml 1.0

Item {
	function updateData(data) {
	    if(data.image)
	    {
	        plot_texture.image = data.image;
            plot_texture.width = data.img_width;
            plot_texture.height = data.img_height;

            plot_texture.anchors.leftMargin = data.widget_width / 2 - plot_texture.width / 2;
            plot_texture.anchors.topMargin = data.widget_height / 2 - plot_texture.height / 2;
	    }

        idle_texture.width = data.icon_width;
        idle_texture.height = data.icon_height;
        idle_texture.source = data.img_path;

        idle_texture.anchors.leftMargin = data.widget_width / 2 - idle_texture.width / 2;
        idle_texture.anchors.topMargin = data.widget_height / 2 - idle_texture.height / 2;
	}

	id: container
		visible: true

	Image {
	    id: idle_texture

	    anchors.left: parent.left
        anchors.top: parent.top
	}

    PlotItem {
        id: plot_texture
    }
}
