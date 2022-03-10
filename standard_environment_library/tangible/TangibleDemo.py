from libPySI import PySI

from plugins.standard_environment_library.SIEffect import SIEffect
from plugins.standard_environment_library._standard_behaviour_mixins.Tangible import Tangible
from plugins.E import E


class TangibleDemo(Tangible):
    regiontype = PySI.EffectType.SI_CUSTOM_NON_DRAWABLE
    regionname = E.id.tangible_demo_regionname
    region_display_name = E.id.tangible_demo_display_name

    def __init__(self, shape=PySI.PointVector(), uuid="", kwargs={}):
        super().__init__(shape, uuid, SIEffect.TEXTURE_PATH_NONE, TangibleDemo.regiontype, TangibleDemo.regionname, kwargs)
        self.color = E.color.tangible_demo_color

    def __update__(self, data):
        super().__update__(data)
        self.shape = data["contour"]

"""
//            if(contour.size() == 4)
    //            {
                  //                const glm::vec3& tlc = contour[0];
//                const glm::vec3& blc = contour[1];
//                const glm::vec3& trc = contour[3];
//
//                glm::vec3 p = trc - tlc;
//                glm::vec3 q = blc - tlc;
//                glm::vec2 xa = glm::normalize(p);
//                glm::vec2 ya = glm::normalize(q);
//
//                float width = glm::length(p);
//                float height = glm::length(q);
//
//                kwargs["x"] = tlc.x;
//                kwargs["y"] = tlc.y;
//                kwargs["x_axis"] = bp::list(bp::make_tuple(xa.x, xa.y));
//                kwargs["y_axis"] = bp::list(bp::make_tuple(ya.x, ya.y));
//                kwargs["width"] = width;
//                kwargs["height"] = height;
//                kwargs["orig_x"] = tobj->outer_contour_geometry_component()->contour()[0].x;
//                kwargs["orig_y"] = tobj->outer_contour_geometry_component()->contour()[0].y;
//                kwargs["orig_width"] = glm::length(tobj->outer_contour_geometry_component()->contour()[3] - tobj->outer_contour_geometry_component()->contour()[0]);
//                kwargs["orig_height"] = glm::length(tobj->outer_contour_geometry_component()->contour()[1] - tobj->outer_contour_geometry_component()->contour()[0]);
//            }
"""