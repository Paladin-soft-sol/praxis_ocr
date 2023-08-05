from rest_framework.response import Response
from rest_framework import status, generics
from ocr_api.models import OcrModel
from ocr_api.serializers import OcrSerializer
import math
from datetime import datetime
from django.core.files.storage import FileSystemStorage
import tabula
import pandas as pd
from datetime import datetime
from uuid import uuid4
import json


class Ocr(generics.GenericAPIView):
    serializer_class = OcrSerializer

    def get(self, request):
        data= OcrModel.objects.all()
        serializer = self.serializer_class(data, many=True)
        return Response({
            "status": "success",
            "data":serializer.data
        },status=status.HTTP_200_OK)
    

    def pdfToExcel(self,ocr_file):
       try:
        df = tabula.read_pdf(ocr_file, pages = 'all', multiple_tables=True,stream=True)
        file_array=[]
        for i in range(len(df)):
            file_name=datetime.now().strftime('%Y%m-%d%H-%M%S-')+ str(uuid4()) +'ocr.xlsx'
            df[i].to_excel('media/'+file_name)
            file_array.append(file_name)
        print("file_array\n",file_array)    
        return json.dumps(file_array)
       except Exception as e:
        print('file error\n',e)
        return False


    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        ocr_file = request.FILES.get('file', False)
        patient_id=request.data.get('patient_id',False)
       
        if patient_id=="":
            return Response({"status":"fail","message": "patient_id is required"},status=status.HTTP_400_BAD_REQUEST)

            
        print("patient_id \n",patient_id)
        print("ocr_file \n",ocr_file)
        if ocr_file==False:          
            return Response({"status":"fail","message": "file is required"},status=status.HTTP_400_BAD_REQUEST)


        if ocr_file:
          file_url=  self.pdfToExcel(ocr_file)
          if file_url==False:
             return Response({"status":"fail","message": "pdf to excel conversion failed"},status=status.HTTP_400_BAD_REQUEST)

             
          request.data._mutable = True
          request.data["lab_report"]=file_url
          serializer = self.serializer_class(data=request.data)
          if serializer.is_valid(): 
             serializer.save()
             return Response({"status": "success","data":serializer.data},status=status.HTTP_200_OK)
    

class OcrDetail(generics.GenericAPIView):
    serializer_class = OcrSerializer

    def getOcrById(self, pk):
         try:
            return OcrModel.objects.get(patient_id=pk)
         except:
            return None

    def get(self, request, pk):
        data = self.getOcrById(pk=pk)
        if data == None:
            return Response({"status": "fail", "message": f"Note with Id: {pk} not found","data":[]}, status=status.HTTP_404_NOT_FOUND)
        else:
            print('data\n',data.lab_report)
            lab_data=json.loads(data.lab_report)
            result=[]
            for i in range(len(lab_data)):
              excel_data_df = pd.read_excel('media/'+lab_data[i])
              json_str = excel_data_df.to_json(orient='records')
              result.extend(json.loads(json_str))
            return Response({"status": "success", "data": result}, status=status.HTTP_200_OK)

