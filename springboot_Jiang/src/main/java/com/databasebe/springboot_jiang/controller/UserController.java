package com.databasebe.springboot_jiang.controller;

import com.databasebe.springboot_jiang.pojo.ResponseMessage;
import com.databasebe.springboot_jiang.service.IUserservice;
import com.databasebe.springboot_jiang.utils.JwtUtill;
import jakarta.validation.constraints.Pattern;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.HashMap;
import java.util.Map;

@RestController
@Validated
@RequestMapping("/user")
public class UserController {
    private final IUserservice userService;

    public UserController(IUserservice userService) {
        this.userService = userService;
    }

    @PostMapping("/register")
    public ResponseMessage register(@Pattern(regexp = "^\\S{5,16}$") String username, @Pattern(regexp = "^\\S{5,16}$")String password){
        //查询用户是否存在
        return userService.register(username,password);
    }
    @PostMapping("/login")
    public ResponseMessage<String> login(@Pattern(regexp = "^\\S{5,16}$") String username, @Pattern(regexp = "^\\S{5,16}$")String password){
        return userService.login(username,password);
    }

    @PostMapping("/Applogin")
    public ResponseMessage<String> Applogin(String password){
        if(!password.equals("Jiang")){
            return ResponseMessage.error(401,"密码错误");
        }else {
            Map<String,Object> claims = new HashMap<>();
            claims.put("appname","Jiang");
            String token = JwtUtill.generateAppToken(claims);
            return ResponseMessage.success(token);
        }
    }



}
