

import io
from PIL import Image
import base64
import plotly
import plotly.express as px
from weasyprint import HTML,CSS

def convert_chart_fig_to_bytes(chart_fig, width, height):
  return plotly.io.to_image(chart_fig, format=None, width=width, height=height, scale=None, validate=True, engine='kaleido')
    
#def encode_to_base64(varobj):
#    return base64.b64encode(varobj)
#  return base64.b64encode(varobj.getvalue()).decode('utf-8')

#def encode_to_base64(varobj):
#    #img = Image.fromarray(varobj, 'RGB')
#    image_bytes=''
#    with io.BytesIO() as buf:
#      varobj.save(buf, 'jpeg')
#      image_bytes = buf.getvalue()
#    #byteimg = io.BytesIO()
#    #varobj.save(byteimg,format="PNG")
#    #byteimg.seek(0)
#    #img_bytes = byteimg.read()
#    return base64.b64encode(image_bytes)

def encode_PIL_Image_to_base64(imgobj):
  im_file = io.BytesIO()
  imgobj.save(im_file, format="JPEG")
  im_bytes = im_file.getvalue()  # im_bytes: image in binary format.
  im_b64 = base64.b64encode(im_bytes)
  return im_b64.decode('utf-8')

def encode_base64_from_bytes(bytesobj):
  return base64.b64encode(bytesobj).decode('utf-8')
    
def download_pdf(uploaded_image, bounding_image, cell_disease_table, RBC_status_table, bar_chart, doughnut_chart, width, height):
  return generate_pdf(encode_PIL_Image_to_base64(uploaded_image), encode_PIL_Image_to_base64(bounding_image), cell_disease_table, RBC_status_table, encode_base64_from_bytes(convert_chart_fig_to_bytes(bar_chart, width, height)), encode_base64_from_bytes(convert_chart_fig_to_bytes(doughnut_chart, width, height)), width, height)

def generate_pdf(uploaded_image, bounding_image,cell_disease_table, RBC_status_table, bar_chart, doughnut_chart, width, height):
  image_height=height
  image_width=width
  bar_chart_width=width
  bar_chart_height=height
  doughnut_chart_width=width
  doughnut_chart_height=height

  cell_disease_table_str='<table><tr>'
  RBC_status_table_str='<table><tr>'

  for i in list(RBC_status_table.columns):
    RBC_status_table_str+=f'<th>{i}</th>'
  
  for i in list(cell_disease_table.columns):
    cell_disease_table_str+=f'<th>{i}</th>'
  
  RBC_status_table_str+='</tr>'
  cell_disease_table_str+='</tr>'

  for index, row in RBC_status_table.iterrows():
    RBC_status_table_str+=f'<td>{round(row["HbA"],2)}</td>'
    RBC_status_table_str+=f'<td>{round(row["HbS"],2)}</td>'
    RBC_status_table_str+=f'<td>{round(row["HbC"],2)}</td>'
    RBC_status_table_str+=f'<td>{row["Status"]}</td></tr>'

  for index, row in cell_disease_table.iterrows():
    cell_disease_table_str+=f'<tr><td>{str(index+1)}</td>'
    cell_disease_table_str+=f'<td>{row["Classes"]}</td>'
    cell_disease_table_str+=f'<td>{row["Count"]}</td>'
    cell_disease_table_str+=f'<td>{row["Percentage"]}</td></tr>'

  RBC_status_table_str+='</table>'
  cell_disease_table_str+='</table>'

#  HTML_TEMPLATE=f"""
#<!DOCTYPE html>
#<html>
#<head>
#<title></title>
#</head>
#<body>
#<div style='content: ""; display: table; clear: both;'>
#  <div style='float: left; width: 50%;'>
#  <span style="font-size:20px; font-weight:bold">Uploaded Image</span>
#  <br>
#  <br>
#  <img class="imagesize" src="data:image/png;base64,{uploaded_image}" alt="uploaded image" />
#  </div>
#  <div style='float: left; width: 50%;'>
#  <span style="font-size:20px; font-weight:bold">Diagnose disease cells</span>
#  <br>     
#  <br>
#  <img class="imagesize" src="data:image/png;base64,{bounding_image}" alt="predicted image" />
#  </div>
#</div>
#<div style='content: ""; display: table; clear: both;'> 
#<span style="font-size:20px; font-weight:bold">Total diagnose detected classified cells are: {cell_disease_table['Count'].sum()}</span>
#</div>
#  <br>
#  <br>
#<div style='content: ""; display: table; clear: both;'> 
#  <span style="font-size:20px; font-weight:bold">Detected cells details</span>
#</div>
#  <br>
#  <br>  
#<div style='content: ""; display: table; clear: both;'>
#  <div style='float: left; width: 50%;'>
#  {cell_disease_table_str}
#  </div>
#  <div style='float: left; width: 50%;'>
#  {RBC_status_table_str}
#  </div>               
#</div>   
#<div style='content: ""; display: table; clear: both;'>
#  <span style="font-size:20px; font-weight:bold">Analysis of detected diseases cells</span>
#</div>
#<div style='content: ""; display: table; clear: both;'>
#  <br>              
#  <img class="barchartsize" src="data:image/png;base64,{bar_chart}"  alt="bar chart image"  />         
#</div>   
#<div style='content: ""; display: table; clear: both;'>
#  <br>
#  <img class="doughnutchartsize" src="data:image/png;base64,{doughnut_chart}" alt="doughnut chart image" />
#</div>
#</div>
#</body>
#</html>
#"""

HTML_TEMPLATE=f"""
<!DOCTYPE html>
<html>
<body style="padding-left:1px;">
<h2>Diagnose Sickle Cell Diseases by Red Blood Cells(RBCs) Classification</h2>
<p style="width: 600px;font-size: 0.67em;font-weight: bold;margin-left:10px;padding:1px;">⚠️
Disclaimer: This app is not intended to be a substitute for professional medical advice, diagnosis, or treatment. The predictions and information provided by the app are for educational and informational purposes only. The predictions are based on a model and may not always be accurate. Users should consult with a qualified healthcare provider before making any decisions based on the apps predictions or information.</p>
<table style="width:100%">
<tr>
  <tr>
    <th>Uploaded Image</th>
    <th>Diagnose disease cells</th>
  </tr>
  <tr>
    <td style="text-align: center; vertical-align: middle;">
  <img class="imagesize" src="data:image/png;base64,{uploaded_image}" alt="uploaded image" />
</td>
<td style="text-align: center; vertical-align: middle;">
<img class="imagesize" src="data:image/png;base64,{bounding_image}" alt="predicted image" /></td>
  </tr>
  <tr>
  <td colspan="2"><p style="font-weight: bold;">Total diagnose detected classified cells are: {cell_disease_table['Count'].sum()}</p></td>
  </tr>
    <tr>
  <td colspan="2"><p style="font-size: 1.2em;font-weight: bold;text-align:center;">Detected cells details</p></td>
  </tr>
  <tr>
    <td style="text-align: center; vertical-align: middle;">
      {cell_disease_table_str}
</td>
    <td style="text-align: center; vertical-align: middle;">
  {RBC_status_table_str}
    </td>
  </tr>
      <tr>
  <td colspan="2">
  <p style="font-size: 1.2em;font-weight: bold;text-align:center;">Analysis of detected diseases cells</p>
  </td>
  </tr>
  <tr>
    <td style="text-align: center; vertical-align: middle;">  
    <img class="barchartsize" src="data:image/png;base64,{bar_chart}"  alt="bar chart image"  />  </td>
    <td style="text-align: center; vertical-align: middle;">
      <img class="doughnutchartsize" src="data:image/png;base64,{doughnut_chart}" alt="doughnut chart image" />
    </td>
  </tr>
</table>
</body>
</html>
"""
  #css=CSS(string=f'''@page {{size: Letter; margin: 0.1in 0.1in 0in 0.1in;}}
  #    img {{border: 5px solid #555;}}
  #    body{{display: block; margin: 0px;}}
  #    .imagesize{{height: {image_height}px; width: {image_width}px; margin: 0 auto;}}  
  #    .barchartsize{{height: {bar_chart_height}px; width: {bar_chart_width}px; margin: 0 auto;}} 
  #    .doughnutchartsize{{height: {doughnut_chart_height}px; width: {doughnut_chart_width}px; margin: 0 auto;}} 
  #     table,th,td{{text-align: center !important; padding: 1px !important; border: 2px solid black !important; border-collapse: collapse !important; font-size: large !important;"}}
  #    .column {{float: left; width: 50%; }}
  #    .row {{ content: ""; display: table; clear: both; }}
  #    ''')

  css=CSS(string=f'''@page {{size: Letter; margin: 0.1in 0.1in 0in 0.1in;}}
      body{{display: block; margin: 0px;}}
      .imagesize{{height: {image_height}px; width: {image_width}px; margin: 0 auto;}}  
      .barchartsize{{height: {bar_chart_height}px; width: {bar_chart_width}px; margin: 0 auto;}} 
      .doughnutchartsize{{height: {doughnut_chart_height}px; width: {doughnut_chart_width}px; margin: 0 auto;}} 
       table,th,td{{text-align: center !important; padding: 1px !important; border: 2px solid black !important; border-collapse: collapse !important; font-size: large !important;"}}
      ''')    

  return HTML_TEMPLATE # HTML(string=HTML_TEMPLATE).write_pdf(optimize_size=(), stylesheets=[css])
