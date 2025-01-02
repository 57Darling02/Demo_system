package com.databasebe.springboot_jiang.utils;

import java.util.Map;

public class sqlUtil {
    public static String buildQuery(Map<String, String> params) {
        StringBuilder sqlBuilder = new StringBuilder("SELECT * FROM monitor_data");

        if (!params.isEmpty()) {
            sqlBuilder.append(" WHERE ");
            int paramCount = 0;
            for (Map.Entry<String, String> entry : params.entrySet()) {
                if (paramCount > 0) {
                    sqlBuilder.append(" AND ");
                }
                sqlBuilder.append(entry.getKey()).append(" = '").append(entry.getValue()).append("'");
                paramCount++;
            }
        }
        return sqlBuilder.toString();
    }
}
