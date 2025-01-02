package com.databasebe.springboot_jiang.interceptors;

import com.databasebe.springboot_jiang.utils.JwtUtill;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import org.springframework.stereotype.Component;
import org.springframework.web.servlet.HandlerInterceptor;


@Component
public class LoginInterceptors implements HandlerInterceptor {
    @Override
    public boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object handler) {
        //令牌验证
        String token = request.getHeader("Authorization");
        try {
            JwtUtill.parseToken(token);
            return true;
        }catch(Exception e){
            response.setStatus(401);
            return false;
        }

    }
}
