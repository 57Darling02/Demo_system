package com.databasebe.springboot_jiang.exception;

import com.databasebe.springboot_jiang.pojo.ResponseMessage;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;


@RestControllerAdvice
public class GlobalExcepptionHandlerAdvice {
    Logger log = LoggerFactory.getLogger(GlobalExcepptionHandlerAdvice.class);
    @ExceptionHandler({Exception.class})
    public ResponseMessage handleException(Exception e, HttpServletRequest request, HttpServletResponse response) {
        log.error("Global error:",e);
        return new ResponseMessage(500,"error",e.getMessage());
//        return ResponseMessage.error(500,"error!something wrong!");
    }


}
