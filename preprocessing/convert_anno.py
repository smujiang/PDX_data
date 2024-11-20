import os

import pandas as pd

xmlHead = '''<Annotations MicronsPerPixel="0.252100">
  <Annotation Id="1" Name="" ReadOnly="0" NameReadOnly="0" LineColorReadOnly="0" Incremental="0" Type="4" LineColor="65280" Visible="1" Selected="1" MarkupImagePath="" MacroName="">
    <Attributes>
      <Attribute Name="Description" Id="0" Value=""/>
    </Attributes>
    <Regions>
      <RegionAttributeHeaders>
        <AttributeHeader Id="9999" Name="Region" ColumnWidth="-1"/>
        <AttributeHeader Id="9997" Name="Length" ColumnWidth="-1"/>
        <AttributeHeader Id="9996" Name="Area" ColumnWidth="-1"/>
        <AttributeHeader Id="9998" Name="Text" ColumnWidth="-1"/>
        <AttributeHeader Id="1" Name="Description" ColumnWidth="-1"/>
      </RegionAttributeHeaders>\n'''
xmlTail = '''    </Regions>
    <Plots/>
  </Annotation>
</Annotations>\n'''

regionStrHead = '''      <Region Id="%d" Type="%d" Text="%s" GeoShape="%s" Zoom="0.042148" Selected="0" ImageLocation="" ImageFocus="0" Length="74565.8" Area="213363186.2" LengthMicrons="18798.0" AreaMicrons="13560170.4" NegativeROA="0" InputRegionId="0" Analyze="1" DisplayId="1">
        <Attributes/>
        <Vertices>\n'''
regionStrTail = '''        </Vertices>
      </Region>\n'''

vertexStr = '''          <Vertex X="%f" Y="%f"/>\n'''

###############################################################

anno_folder = "annotation_example"
extension = ".csv"


fn_list = [f for f in os.listdir(anno_folder) if f.endswith(extension)]

print(fn_list)
for f in fn_list:
    fn = os.path.join(anno_folder, f)

    df = pd.read_csv(fn, sep=',')  #
    roi_names = set(df["ROI_Name"])

    sv_fn = os.path.join(anno_folder, "convert_" + f.replace(extension, ".xml"))

    xml_fh = open(sv_fn, 'w')
    wrt_str = xmlHead

    for idx, roi_n in enumerate(roi_names):
        region_str = regionStrHead % (idx, idx, roi_n, "Polygon")
        wrt_str += region_str
        xy_df = df[df["ROI_Name"]==roi_n]
        x, y = xy_df["X_base"], xy_df["Y_base"]
        for idx_x, xx in enumerate(x):
            str_points = vertexStr % (xx, y[idx_x])
            wrt_str += str_points

        wrt_str += regionStrTail

    wrt_str += xmlTail
    xml_fh.write(wrt_str)
    xml_fh.close()








