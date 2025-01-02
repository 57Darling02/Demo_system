package com.databasebe.springboot_jiang;

import com.auth0.jwt.JWT;
import com.auth0.jwt.JWTVerifier;
import com.auth0.jwt.algorithms.Algorithm;
import com.auth0.jwt.interfaces.DecodedJWT;
import org.junit.jupiter.api.Test;
import java.util.Date;
import java.util.HashMap;
import java.util.Map;

public class jwttest {
    @Test
    public void testGen(){
        Map<String,Object> claim = new HashMap<>();
        claim.put("id",1);
        claim.put("username","admin");
        String token = JWT.create()
                .withClaim("user",claim)
                        .withExpiresAt(new Date(System.currentTimeMillis()+1000*60*60))
                                .sign(Algorithm.HMAC256("Jiang"));

        System.out.println(token);
    }
    @Test
    public void testVerify(){
        String token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjp7ImlkIjoxLCJ1c2VybmFtZSI6ImFkbWluIn0sImV4cCI6MTczNTEwMjQyOX0.Uf9z5_NC4wAi1yGpQHllCELvODmP7o1XCdNjWyjf4dc";

        JWTVerifier verifier = JWT.require(Algorithm.HMAC256("Jiang")).build();
        DecodedJWT jwt = verifier.verify(token);
        System.out.println(jwt.getClaim("user").asMap());
    }

}
