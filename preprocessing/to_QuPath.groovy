/*
* Copied from https://gist.github.com/DanaCase/9cfc23912fee48e437af03f97763d78e
* Convert the annotation file (xml files) from Aperio Image Scope, so that the annotation can be loaded into QuPath
* Also check this link: https://groups.google.com/forum/#!searchin/qupath-users/import$20annotation%7Csort:date/qupath-users/xhCx_nhbWQQ/0kW38lEXCAAJ
*/

// Update notes:
// Code modified for QuPath v0.5.0. smujiang@gmail.com, 11-18-2024

import groovy.xml.*
import qupath.lib.scripting.QP
import qupath.lib.geom.Point2
import qupath.lib.roi.PolygonROI
import qupath.lib.objects.PathAnnotationObject
import qupath.lib.images.servers.ImageServer
import qupath.fx.dialogs.FileChoosers

//Aperio Image Scope displays images in a different orientation
def rotated = true

def server = QP.getCurrentImageData().getServer()
def h = server.getHeight()
def w = server.getWidth()

// need to add annotations to hierarchy so qupath sees them
def hierarchy = QP.getCurrentHierarchy()


//Prompt user for exported aperio image scope annotation file
// Choose multiple files. Need add a for loop for the files -> file
//def files = FileChoosers.promptForMultipleFiles("Choose input files",
//            FileChoosers.createExtensionFilter("xml files", ".xml"))

// Choose one file
def file = FileChoosers.promptForFile("Choose input file",
            FileChoosers.createExtensionFilter("xml files", ".xml"))
//def directory = getQuPath().getDialogHelper().promptForDirectory(null)
//def file = getQuPath().getDialogHelper().promptForFile(directory)
def text = file.getText()

def list = new XmlSlurper().parseText(text)


list.Annotation.each {

    it.Regions.Region.each { region ->

        def tmp_points_list = []

        region.Vertices.Vertex.each{ vertex ->

            if (rotated) {
                X = vertex.@Y.toDouble()
                Y = h - vertex.@X.toDouble()
            }
            else {
                X = vertex.@X.toDouble()
                Y = vertex.@Y.toDouble()
            }
            tmp_points_list.add(new Point2(X, Y))
        }

        def roi = new PolygonROI(tmp_points_list)

        def annotation = new PathAnnotationObject(roi)

        hierarchy.addObject(annotation, false)
    }
}
