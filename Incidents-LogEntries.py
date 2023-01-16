### DEVELOPED BY PAGERDUTY PROFESSIONAL SERVICES/SUCCESS ON DEMAND
### THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
### IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
### FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
### AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
### LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
### OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
### THE SOFTWARE.

### This code gets all  & alerts for every incident

from pdpyras import APISession
import pandas as pd
from datetime import datetime, timedelta
from dateutil.relativedelta import *

API_ACCESS_KEY = 'YOUR API KEY HERE'
session = APISession(API_ACCESS_KEY)
list_incidents = pd.DataFrame()
list_log_entries = pd.DataFrame()
offset = 0
days_to_get = 1  # three months Data
today = datetime.today()
start_date = today - relativedelta(days=int(days_to_get - 1))
# declare the days that you want to go back asking for incidents

for x in range(days_to_get):
    offset = 0
    start = start_date + relativedelta(days=int(x))
    end = start_date + relativedelta(days=int(x + 1))

    response = session.get(
        "/incidents?since=" + str(start)[0:10] + "&until=" + str(end)[0:10] + "&limit=100&total=true&offset=" + str(
            offset))
    dataframe_incidents = pd.json_normalize(response.json()["incidents"], max_level=None)
    list_incidents = pd.concat([list_incidents, dataframe_incidents], ignore_index=True, axis=0)

    # this is going to fill the list_incidents dataframe with pagination

    while response.json()["more"] and offset < 9900:  # more than 10.000 record would fail
        limit = response.json()["limit"]
        offset = offset + int(limit)
        response = session.get("/incidents?since=" + str(start)[0:10] + "&until=" + str(end)[0:10] + "&limit=100&total=true&offset=" + str(offset))
        dataframe_incidents = pd.json_normalize(response.json()["incidents"], max_level=None)
        list_incidents = pd.concat([list_incidents, dataframe_incidents], ignore_index=True, axis=0)
print(len(list_incidents))

for s in range(len(list_incidents)):
    response = session.get("/incidents/" + str(list_incidents.id[s]) + "/log_entries?is_overview=false")
    dataframe_log_entries = pd.json_normalize(response.json()["log_entries"], max_level=None)
    dataframe_log_entries["IncidentID"] = list_incidents.id[s]
    list_log_entries = pd.concat([list_log_entries, dataframe_log_entries], ignore_index=True, axis=0)


print(list_incidents)
print(list_log_entries)

df1 = list_log_entries
df1.to_csv('logs.csv')

df1 = list_incidents
df1.to_csv('incidents.csv')

today2 = datetime.today()
execution_time = today2 - today
print(execution_time)