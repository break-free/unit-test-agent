import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.BeforeEach;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;
import org.apache.fineract.integrationtests.common.system.CodeHelper;
import io.restassured.specification.RequestSpecification;
import io.restassured.specification.ResponseSpecification;

import java.util.HashMap;
import java.util.List;

import static org.mockito.Mockito.*;

public class CodeHelperTest {

    @InjectMocks
    CodeHelper codeHelper;

    @Mock
    RequestSpecification requestSpec;

    @Mock
    ResponseSpecification responseSpec;

    @BeforeEach
    public void init() {
        MockitoAnnotations.initMocks(this);
    }

    @Test
    public void testRetrieveOrCreateCodeValue_WhenCodeValuesListIsEmpty() {
        when(CodeHelper.getCodeValuesForCode(requestSpec, responseSpec, anyInt(), anyString())).thenReturn(List.of());
        HashMap<String, Object> result = codeHelper.retrieveOrCreateCodeValue(1, requestSpec, responseSpec);
        verify(CodeHelper, times(1)).createCodeValue(any(), any(), anyInt(), anyString(), anyInt(), anyString());
    }

    @Test
    public void testRetrieveOrCreateCodeValue_WhenCodeValuesListIsNotEmpty() {
        HashMap<String, Object> mockCodeValue = new HashMap<>();
        when(CodeHelper.getCodeValuesForCode(requestSpec, responseSpec, anyInt(), anyString())).thenReturn(List.of(mockCodeValue));
        HashMap<String, Object> result = codeHelper.retrieveOrCreateCodeValue(1, requestSpec, responseSpec);
        verify(CodeHelper, times(0)).createCodeValue(any(), any(), anyInt(), anyString(), anyInt(), anyString());
    }

    @Test
    public void testRetrieveOrCreateCodeValue_WhenCodeValuesListIsNull() {
        when(CodeHelper.getCodeValuesForCode(requestSpec, responseSpec, anyInt(), anyString())).thenReturn(null);
        HashMap<String, Object> result = codeHelper.retrieveOrCreateCodeValue(1, requestSpec, responseSpec);
        verify(CodeHelper, times(1)).createCodeValue(any(), any(), anyInt(), anyString(), anyInt(), anyString());
    }
}
