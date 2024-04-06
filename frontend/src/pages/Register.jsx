import React from 'react';
import Button from '@mui/material/Button';
import InputLabel from '@mui/material/InputLabel';
import InputAdornment from '@mui/material/InputAdornment';
import FormControl from '@mui/material/FormControl';
import OutlinedInput from '@mui/material/OutlinedInput';
import { FaUserCircle, FaKey } from 'react-icons/fa';
import IconButton from '@mui/material/IconButton';
import { MdOutlineVisibility, MdOutlineVisibilityOff } from 'react-icons/md';
import axios from 'axios';
import { toast } from 'react-hot-toast';
import { useNavigate } from 'react-router-dom';
import { useState } from 'react';
const Login = () => {
  const [showPassword, setShowPassword] = React.useState(false);
  const [PassMatch, setPassMatch] = React.useState(true);
  const navigate = useNavigate();
  const handleClickShowPassword = () => setShowPassword((show) => !show);

  const [UserData, setUserData] = React.useState({
    email: '',
    password: '',
    confirmpass: '',
  });
  const AllFieldsAreFilled =
    UserData.email != '' &&
    UserData.password != '' &&
    UserData.confirmpass != '';
  const handleDataChange = (event) => {
    const { name, value } = event.target;
    setUserData({ ...UserData, [name]: value });
  };

  const handleMouseDownPassword = (event) => {
    event.preventDefault();
  };

  const handleSubmit = async () => {
    await axios
      .post('http://127.0.0.1:5000/register', UserData)
      .then((res) => {
        console.log(res.status);
        if (res.status == 200) {
          localStorage.setItem('access_token', res.data.access_token);
          localStorage.setItem('userID', res.data.user_id);
          alert('User Successfully registered. Welcome!');
          navigate('/dashboard');
        } else if (String(res.status) == '400') {
          toast.error(res.data.msg, {
            duration: 4000,
            position: 'top-center',
          });
        } else if (res.status == 402) {
          toast.error('User already exists', {
            duration: 4000,
            position: 'top-center',
          });
        }
        console.log(res);
      })
      .catch((err) => {
        console.log(err);
        if (err.response.status == 400) {
          alert(err.response.data.msg);
        } else if (err.response.status == 402) {
          toast.error('User already exists', {
            duration: 4000,
            position: 'top-center',
          });
        }
      });
  };

  return (
    <div className="bg-[#E5E5E5] min-w-[1920px] min-h-[100vh] m-[0] text-black">
      <div>
        <h1 className="font-poppins font-bold text-[48px] ml-[600px] pt-[80px]">
          Register
        </h1>
      </div>
      <div className="ml-[114px] mt-[60px] flex flex-col gap-[20px]">
        <div className="flex flex-col gap-[10px]">
          <span className="font-poppins font-semibold text-[20px]">Email</span>
          <FormControl variant="standard">
            <OutlinedInput
              id="input-with-icon-adornment"
              className="max-w-[1146px]"
              placeholder="Enter your registered Email"
              value={UserData.email}
              onChange={(e) => handleDataChange(e)}
              name="email"
              required={true}
              startAdornment={
                <InputAdornment position="start">
                  <FaUserCircle />
                </InputAdornment>
              }
            />
          </FormControl>
        </div>
        <div className="flex flex-col gap-[10px]">
          <span className="font-poppins font-semibold text-[20px]">
            Password
          </span>
          <FormControl sx={{ m: 0, width: '1146px' }} variant="outlined">
            <InputLabel htmlFor="outlined-adornment-password">
              Password
            </InputLabel>
            <OutlinedInput
              id="outlined-adornment-password"
              className={`${PassMatch ? 'border-red-600' : ''}`}
              type={showPassword ? 'text' : 'password'}
              onChange={(e) => handleDataChange(e)}
              value={UserData.password}
              required={true}
              endAdornment={
                <InputAdornment position="end">
                  <IconButton
                    aria-label="toggle password visibility"
                    onClick={handleClickShowPassword}
                    onMouseDown={handleMouseDownPassword}
                    edge="end"
                  >
                    {showPassword ? (
                      <MdOutlineVisibilityOff />
                    ) : (
                      <MdOutlineVisibility />
                    )}
                  </IconButton>
                </InputAdornment>
              }
              name="password"
            />
          </FormControl>
        </div>
        <div className="flex flex-col gap-[10px]">
          <span className="font-poppins font-semibold text-[20px]">
            Re-Enter Password
          </span>
          <FormControl sx={{ m: 0, width: '1146px' }} variant="outlined">
            <InputLabel htmlFor="outlined-adornment-password">
              Password
            </InputLabel>
            <OutlinedInput
              id="outlined-adornment-password"
              className={`${PassMatch ? 'border-red-600' : ''}`}
              type={showPassword ? 'text' : 'password'}
              value={UserData.confirmpass}
              onChange={(e) => handleDataChange(e)}
              required={true}
              endAdornment={
                <InputAdornment position="end">
                  <IconButton
                    aria-label="toggle password visibility"
                    onClick={handleClickShowPassword}
                    onMouseDown={handleMouseDownPassword}
                    edge="end"
                  >
                    {showPassword ? (
                      <MdOutlineVisibilityOff />
                    ) : (
                      <MdOutlineVisibility />
                    )}
                  </IconButton>
                </InputAdornment>
              }
              name="confirmpass"
            />
          </FormControl>
        </div>
      </div>

      <div className="mt-[40px] ml-[650px]">
        <Button
          variant="outlined"
          color="success"
          disabled={!AllFieldsAreFilled}
          onClick={() => handleSubmit()}
        >
          {' '}
          Submit{' '}
        </Button>
      </div>
    </div>
  );
};

export default Login;
