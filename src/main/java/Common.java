import java.io.IOException;
import java.lang.*;
import java.sql.*;
import java.util.*;
import java.util.stream.Collectors;
import java.io.InputStream;

import net.dean.jraw.RedditClient;
import net.dean.jraw.http.UserAgent;
import net.dean.jraw.http.oauth.Credentials;
import net.dean.jraw.http.oauth.OAuthData;
import net.dean.jraw.http.oauth.OAuthException;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import net.dean.jraw.models.LoggedInAccount;
import net.dean.jraw.models.Submission;
import net.dean.jraw.paginators.SubredditPaginator;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;


/**
 * Created by marshall humble on 7/10/16.
 */

public class Common {

    private static Logger logger = LoggerFactory.getLogger(Common.class);
    private static UserAgent myUserAgent = UserAgent.of("desktop", "mod_app", "v0.1", "");
    private static RedditClient redditClient = new RedditClient(myUserAgent);

    public static void main(String[] args) {
        Set<String> urls = getLinks(5, "");

        if (urls != null) {
            System.out.println(urls.toString());
        }
    }

    static boolean doLogin() {

        Credentials credentials = null;

        try {
            credentials = getCredentials();
        } catch (IOException e) {
            e.printStackTrace();
        }

        boolean isLoggedIn = false;

        if (credentials != null) {

            try {
                OAuthData authData = redditClient.getOAuthHelper().easyAuth(credentials);
                redditClient.authenticate(authData);
                LoggedInAccount acc = redditClient.me();
                isLoggedIn = acc.getDataNode() != null;
            } catch (OAuthException e) {
                logger.debug(String.valueOf(e));
            }
        }

        return isLoggedIn;
    }

    private static Credentials getCredentials() throws IOException {

        Credentials credentials;
        String username = null, password = null, scriptId = null, scriptSecret =null;

        InputStream in = Common.class.getResourceAsStream("/credentials.json");

        if (in == null) {
            throw new IOException("credentials.json could not be found.");
        }

        JsonNode data = null;

        try {
            data = new ObjectMapper().readTree(in);
        } catch (IOException e) {
            logger.debug("Could not read credentials.json ", e);
        }

        if (data != null) {
            username = data.get("user").get("username").asText();
            password = data.get("user").get("password").asText();
            scriptId = data.get("script").get("client_id").asText();
            scriptSecret = data.get("script").get("client_secret").asText();
        }

        credentials = Credentials.script(username, password, scriptId, scriptSecret);

        return credentials;
    }

    static Set<String> getLinks(int linkLimit, String subredditName) {
        boolean checkLoggedIn = doLogin();
        Set<String> linkedStories = new HashSet<>();

        if (checkLoggedIn) {

            SubredditPaginator subreddit = new SubredditPaginator(redditClient, subredditName);

            if (linkLimit != 0) {
                subreddit.setLimit(linkLimit);
                linkedStories.addAll(subreddit.next().stream().map(Submission::getUrl).collect(Collectors.toList()));
            } else {
                linkedStories.addAll(subreddit.next().stream().map(Submission::getUrl).collect(Collectors.toList()));
            }
        }
        return linkedStories;
    }

    static boolean setupNewDB(String fileName) {
        final String url = "jdbc:sqlite:../" + "resources" + fileName;
        boolean dbIsSetup = false;

        try (Connection conn = DriverManager.getConnection(url)) {
            if (conn != null) {
                DatabaseMetaData meta = conn.getMetaData();
                logger.info("A new {} database has been created {} .", meta, fileName);
                dbIsSetup = true;
            }

        } catch (SQLException e) {
            logger.debug(e.getMessage());
        }

        return dbIsSetup;
    }

    static boolean createNewTable(String dbname, String tableName, String primaryKey) {
        boolean tableIsSetup = false;

        // SQLite connection string
        String url = "jdbc:sqlite:../" + "resources/" + dbname;

        // SQL statement for creating a new table
        String sql = "CREATE TABLE IF NOT EXISTS" + tableName + "(\n"
                + "	id INTEGER PRIMARY KEY,\n"
                + "	name text NOT NULL,\n"
                + "	capacity real\n"
                + ");";

        try (Connection conn = DriverManager.getConnection(url);
             Statement stmt = conn.createStatement()) {
            // create a new table
            stmt.execute(sql);
            tableIsSetup = true;
        } catch (SQLException e) {
            logger.debug(e.getMessage());
        }

        return tableIsSetup;
    }
}
