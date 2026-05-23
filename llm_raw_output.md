# LLM Output

=== FILE: src/App.jsx ===
import React, { useState, useEffect } from 'react';
import { HashRouter, Routes, Route, Link } from 'react-router-dom';
import axios from 'axios';
import { ToastContainer } from 'react-toastify';
import { toast } from 'react-toastify';
import { notify } from 'react-hot-toast';
import { FiCalendar } from 'react-icons/fi';
import { AiOutlineUser } from 'react-icons/ai';
import { format } from 'date-fns';
import { useForm } from 'react-hook-form';
import { clsx } from 'clsx';

const BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

function App() {
  const [doctors, setDoctors] = useState([]);
  const [appointments, setAppointments] = useState([]);
  const [schedules, setSchedules] = useState([]);
  const [patient, setPatient] = useState({});
  const { register, handleSubmit, reset } = useForm();

  useEffect(() => {
    axios.get(`${BASE_URL}/doctors`)
      .then(response => {
        setDoctors(response.data);
      })
      .catch(error => {
        console.error(error);
      });

    axios.get(`${BASE_URL}/appointments`)
      .then(response => {
        setAppointments(response.data);
      })
      .catch(error => {
        console.error(error);
      });

    axios.get(`${BASE_URL}/schedules`)
      .then(response => {
        setSchedules(response.data);
      })
      .catch(error => {
        console.error(error);
      });
  }, []);

  const handleRegister = (data) => {
    axios.post(`${BASE_URL}/patients`, data)
      .then(response => {
        setPatient(response.data);
        notify('Patient registered successfully');
      })
      .catch(error => {
        console.error(error);
      });
  };

  const handleBookAppointment = (data) => {
    axios.post(`${BASE_URL}/appointments`, data)
      .then(response => {
        setAppointments([...appointments, response.data]);
        notify('Appointment booked successfully');
      })
      .catch(error => {
        console.error(error);
      });
  };

  const handleViewSchedule = (doctorId) => {
    axios.get(`${BASE_URL}/schedules/${doctorId}`)
      .then(response => {
        setSchedules(response.data);
      })
      .catch(error => {
        console.error(error);
      });
  };

  return (
    <HashRouter>
      <ToastContainer />
      <div className="container mx-auto p-4 pt-6 md:p-6 lg:p-12 xl:p-24">
        <h1 className="text-3xl font-bold mb-4">Hospital Appointment Booking System</h1>
        <Routes>
          <Route path="/" element={
            <div>
              <h2 className="text-2xl font-bold mb-4">Patient Registration</h2>
              <form onSubmit={handleSubmit(handleRegister)}>
                <div className="mb-4">
                  <label className="block text-sm font-medium mb-2">Name</label>
                  <input type="text" {...register("name")} className="block w-full p-2 pl-10 text-sm text-gray-700 border border-gray-200 rounded-lg focus:ring-blue-500 focus:border-blue-500" />
                </div>
                <div className="mb-4">
                  <label className="block text-sm font-medium mb-2">Email</label>
                  <input type="email" {...register("email")} className="block w-full p-2 pl-10 text-sm text-gray-700 border border-gray-200 rounded-lg focus:ring-blue-500 focus:border-blue-500" />
                </div>
                <div className="mb-4">
                  <label className="block text-sm font-medium mb-2">Phone</label>
                  <input type="tel" {...register("phone")} className="block w-full p-2 pl-10 text-sm text-gray-700 border border-gray-200 rounded-lg focus:ring-blue-500 focus:border-blue-500" />
                </div>
                <button type="submit" className="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800">Register</button>
              </form>
            </div>
          } />
          <Route path="/doctors" element={
            <div>
              <h2 className="text-2xl font-bold mb-4">Doctors</h2>
              <ul>
                {doctors.map((doctor) => (
                  <li key={doctor.id} className="mb-4">
                    <Link to={`/doctors/${doctor.id}/schedule`}>{doctor.name}</Link>
                  </li>
                ))}
              </ul>
            </div>
          } />
          <Route path="/doctors/:id/schedule" element={
            <div>
              <h2 className="text-2xl font-bold mb-4">Doctor Schedule</h2>
              <button onClick={() => handleViewSchedule(patient.doctorId)} className="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800">View Schedule</button>
              <ul>
                {schedules.map((schedule) => (
                  <li key={schedule.id} className="mb-4">
                    <span className="mr-2">{format(schedule.date, 'yyyy-MM-dd')}</span>
                    <span className="mr-2">{schedule.time}</span>
                    <button onClick={() => handleBookAppointment({ patientId: patient.id, doctorId: schedule.doctorId, date: schedule.date, time: schedule.time })} className="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800">Book Appointment</button>
                  </li>
                ))}
              </ul>
            </div>
          } />
          <Route path="/appointments" element={
            <div>
              <h2 className="text-2xl font-bold mb-4">Appointments</h2>
              <ul>
                {appointments.map((appointment) => (
                  <li key={appointment.id} className="mb-4">
                    <span className="mr-2">{appointment.patientName}</span>
                    <span className="mr-2">{appointment.doctorName}</span>
                    <span className="mr-2">{format(appointment.date, 'yyyy-MM-dd')}</span>
                    <span className="mr-2">{appointment.time}</span>
                  </li>
                ))}
              </ul>
            </div>
          } />
        </Routes>
      </div>
    </HashRouter>
  );
}

export default App;
=== END ===

=== FILE: src/main.jsx ===
import React from 'react';
import ReactDOM from 'react-dom';
import App from './App';

ReactDOM.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
  document.getElementById('root')
);
=== END ===

=== FILE: src/index.css ===
@tailwind base;
@tailwind components;
@tailwind utilities;
=== END ===

=== FILE: src/api.js ===
const BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

export const getDoctors = async () => {
  const response = await fetch(`${BASE_URL}/doctors`);
  return response.json();
};

export const getAppointments = async () => {
  const response = await fetch(`${BASE_URL}/appointments`);
  return response.json();
};

export const getSchedules = async (doctorId) => {
  const response = await fetch(`${BASE_URL}/schedules/${doctorId}`);
  return response.json();
};

export const registerPatient = async (data) => {
  const response = await fetch(`${BASE_URL}/patients`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(data)
  });
  return response.json();
};

export const bookAppointment = async (data) => {
  const response = await fetch(`${BASE_URL}/appointments`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(data)
  });
  return response.json();
};
=== END ===