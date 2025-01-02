package com.databasebe.springboot_jiang.config;

import com.databasebe.springboot_jiang.interceptors.LoginInterceptors;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.servlet.config.annotation.InterceptorRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;

@Configuration
public class WebConfig implements WebMvcConfigurer {
    private final LoginInterceptors loginInterceptors;

    public WebConfig(LoginInterceptors loginInterceptors) {
        this.loginInterceptors = loginInterceptors;
    }

    @Override
    public void addInterceptors(InterceptorRegistry registry) {
        registry.addInterceptor(loginInterceptors).excludePathPatterns("/monitor/login","/user/login","/user/register","/user/Applogin");
    }
}
