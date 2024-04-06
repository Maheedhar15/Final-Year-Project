import React from 'react';
import Button from '@mui/material/Button';
import InputLabel from '@mui/material/InputLabel';
import InputAdornment from '@mui/material/InputAdornment';
import FormControl from '@mui/material/FormControl';
import OutlinedInput from '@mui/material/OutlinedInput';
import { FaUserCircle, FaKey } from 'react-icons/fa';
import { toast } from 'react-hot-toast';
import axios from 'axios';
import IconButton from '@mui/material/IconButton';
import { MdOutlineVisibility, MdOutlineVisibilityOff } from 'react-icons/md';
import { useNavigate } from 'react-router-dom';
const ForgotPass = () => {
  const [showPassword, setShowPassword] = React.useState(false);

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
  const navigate = useNavigate();
  const handleSubmit = async () => {
    await axios
      .post('http://127.0.0.1:5000/forgotpassword', UserData)
      .then((res) => {
        console.log(res.status);
        if (res.status == 200) {
          alert(res.data.message);
          navigate('/');
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
          alert(err.response.data.message);
        } else if (err.response.status == 404) {
          alert(err.response.data.message);
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
              value={UserData.email}
              placeholder="Enter your registered Email"
              onChange={(e) => handleDataChange(e)}
              name="email"
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
            New Password
          </span>
          <FormControl sx={{ m: 0, width: '1146px' }} variant="outlined">
            <InputLabel htmlFor="outlined-adornment-password">
              New Password
            </InputLabel>
            <OutlinedInput
              id="outlined-adornment-password"
              className=""
              value={UserData.password}
              type={showPassword ? 'text' : 'password'}
              onChange={(e) => handleDataChange(e)}
              name="password"
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
              placeholder="Enter your new password"
            />
          </FormControl>
        </div>
        <div className="flex flex-col gap-[10px]">
          <span className="font-poppins font-semibold text-[20px]">
            Re-Enter New Password
          </span>
          <FormControl sx={{ m: 0, width: '1146px' }} variant="outlined">
            <InputLabel htmlFor="outlined-adornment-password">
              Re-Enter New Password
            </InputLabel>
            <OutlinedInput
              id="outlined-adornment-password"
              className=""
              value={UserData.confirmpass}
              type={showPassword ? 'text' : 'password'}
              onChange={(e) => handleDataChange(e)}
              name="confirmpass"
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
              placeholder="Re-Enter your new password"
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

export default ForgotPass;
