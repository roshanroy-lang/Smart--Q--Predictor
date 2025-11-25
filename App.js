import React, {useEffect, useState} from 'react';
import axios from 'axios';

const API_BASE = process.env.REACT_APP_API || "http://localhost:8000";

function App(){
  const [data, setData] = useState({people_in_queue:0, estimated_wait_time_minutes:0});
  const [loading,setLoading]=useState(false);

  const fetchData = async () => {
    setLoading(true);
    try{
      const res = await axios.get(`${API_BASE}/waiting-time`);
      setData(res.data);
    }catch(e){
      console.error(e);
    }finally{
      setLoading(false);
    }
  };

  useEffect(()=>{
    fetchData();
    const iv = setInterval(fetchData, 5000);
    return ()=> clearInterval(iv);
  },[]);

  return (
    <div style={{fontFamily:'Arial',padding:20}}>
      <h1>Smart Queue - Live Viewer</h1>
      <div style={{fontSize:18, marginTop:10}}>
        <div>People in queue: <strong>{data.people_in_queue}</strong></div>
        <div>Estimated wait (minutes): <strong>{data.estimated_wait_time_minutes}</strong></div>
      </div>
      <button onClick={fetchData} style={{marginTop:20}}>Refresh</button>
      {loading && <div>Loading...</div>}
    </div>
  );
}

export default App;
