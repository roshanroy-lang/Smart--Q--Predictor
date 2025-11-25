import React, {useState} from 'react';
import axios from 'axios';
const API_BASE = process.env.REACT_APP_API || "http://localhost:8000";

export default function AdminApp(){
  const [avgTime, setAvgTime] = useState(4);
  const [msg, setMsg] = useState('');

  const save = async () => {
    try{
      const res = await axios.post(`${API_BASE}/admin/set-service-time`, {average_service_time_minutes: Number(avgTime)});
      setMsg('Saved: ' + JSON.stringify(res.data));
    }catch(e){
      setMsg('Error saving');
    }
  };

  return (
    <div style={{padding:20,fontFamily:'Arial'}}>
      <h1>Admin Dashboard</h1>
      <div style={{marginTop:10}}>
        <label>Average service time (minutes): </label>
        <input value={avgTime} onChange={e=>setAvgTime(e.target.value)} style={{width:60, marginLeft:10}}/>
        <button onClick={save} style={{marginLeft:10}}>Save</button>
      </div>
      <div style={{marginTop:20}}>{msg}</div>
    </div>
  );
}
