package com.databasebe.springboot_jiang.utils;

import com.auth0.jwt.JWT;
import com.auth0.jwt.algorithms.Algorithm;

import java.util.Date;
import java.util.Map;

public class JwtUtill {
    private static final String SECRET_KEY = "znys2201";
    public static String generateToken(Map<String,Object> claims) {
        // 生成JWT令牌
        // 这里使用了一个简单的示例，实际应用中需要使用更安全的算法和密钥
        return JWT.create()
                .withClaim("claims",claims)
                .withExpiresAt(new Date(System.currentTimeMillis()+1000*60*60))
                .sign(Algorithm.HMAC256(SECRET_KEY));
    }
    public static String generateAppToken(Map<String,Object> claims) {
        // 生成JWT令牌
        // 这里使用了一个简单的示例，实际应用中需要使用更安全的算法和密钥
        return JWT.create()
                .withClaim("claims",claims)
                .sign(Algorithm.HMAC256(SECRET_KEY));
    }


    public static Map<String,Object> parseToken(String token) {
        // 验证JWT令牌
        // 这里使用了一个简单的示例，实际应用中需要使用更安全的算法和密钥
        return JWT.require(Algorithm.HMAC256(SECRET_KEY))
                .build()
                .verify(token)
                .getClaim("claims")
                .asMap();
    }
}
