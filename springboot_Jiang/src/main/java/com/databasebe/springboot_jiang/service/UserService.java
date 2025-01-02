package com.databasebe.springboot_jiang.service;

import com.databasebe.springboot_jiang.mapper.UserMapper;

import com.databasebe.springboot_jiang.pojo.ResponseMessage;
import com.databasebe.springboot_jiang.pojo.User;
import com.databasebe.springboot_jiang.utils.JwtUtill;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.HashMap;
import java.util.Map;


@Service
public class UserService implements IUserservice{
    @Autowired
    private UserMapper userMapper;


    @Override
    public ResponseMessage login(String username, String password) {
        User loggingUser = userMapper.findByUsername(username);
        if (loggingUser == null){
            return ResponseMessage.error(401,"用户不存在");
        }
        if(!loggingUser.getPassword().equals(password)){
            return ResponseMessage.error(401,"密码错误");
        }else {
            Map<String,Object> claims = new HashMap<>();
            claims.put("username",loggingUser.getUsername());
            claims.put("id",loggingUser.getId());
            String token = JwtUtill.generateToken(claims);
            return ResponseMessage.success(token);
        }
    }

    @Override
    public ResponseMessage register(String username, String password) {
        User u = userMapper.findByUsername(username);
        if(u != null){
            return ResponseMessage.error(500,"用户已存在");
        }else{
            userMapper.register(username,password);
            return ResponseMessage.success(u);
        }
    }
}
