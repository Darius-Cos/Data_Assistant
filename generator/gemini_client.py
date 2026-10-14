import os
import vertexai
from vertexai.generative_models import GenerativeModel

 #os.getenv(key, default)
# in case that we wanna change the GCP_PROJECT_ID in the future to be more easily
vertexai.init(
    project=os.getenv("GCP_PROJECT_ID", "gd-gcp-gridu-genai"),
    location=os.getenv("GCP_LOCATION", "us-central1"),
)

# Aceasta se afla în afara oricarei funcții. 
# Cand pornesti aplicația Streamlit, 
# Python citeste fișierul tău si execută aceasta linie pe loc.
#  Modelul este creat și stocat în memoria RAM într-o variabilă 
# numita MODEL înainte ca tu să apeși pe vreun buton în interfață.


MODEL = GenerativeModel("gemini-2.0-flash")
#Când apelezi get_model(), Python nu mai creează nimic nou. Doar se uită în memorie,
# vede că MODEL există deja și ți-l "întinde" imediat.
def get_model():
    return MODEL


