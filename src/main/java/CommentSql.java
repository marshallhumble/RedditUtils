
import java.io.IOException;
import java.lang.*;
import java.sql.*;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;


/**
 * Created by marshall humble on 8/13/16.
 */
public class CommentSql {
    private static Logger logger = LoggerFactory.getLogger(CommentSql.class);

    public static void main(String[] args) throws IOException {
        final boolean isLoggedIn = Common.doLogin();
        if (isLoggedIn) {
            logger.info("We are logged in");
        }
    }
}

