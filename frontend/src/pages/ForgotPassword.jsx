import React from 'react';
import Button from '@mui/material/Button';
import InputLabel from '@mui/material/InputLabel';
import InputAdornment from '@mui/material/InputAdornment';
import FormControl from '@mui/material/FormControl';
import OutlinedInput from '@mui/material/OutlinedInput';
import { FaUserCircle, FaKey } from 'react-icons/fa';
import IconButton from '@mui/material/IconButton';
import { MdOutlineVisibility, MdOutlineVisibilityOff } from 'react-icons/md';
const Login = () => {
  const [showPassword, setShowPassword] = React.useState(false);

  const handleClickShowPassword = () => setShowPassword((show) => !show);

  const handleMouseDownPassword = (event) => {
    event.preventDefault();
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
              type={showPassword ? 'text' : 'password'}
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
              type={showPassword ? 'text' : 'password'}
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
        <Button variant="outlined" color="success">
          {' '}
          Submit{' '}
        </Button>
      </div>
    </div>
  );
};

export default Login;
